from flask import Flask, request, jsonify, render_template
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from huggingface_hub import login
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from dotenv import load_dotenv
import certifi
import os

load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

login(token=hf_token)

app = Flask(__name__)

chat_model = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    task="text-generation",
    temperature=0.1,
    max_new_tokens=512
)

model = ChatHuggingFace(llm=chat_model)

class BlogState(TypedDict):
    title: str
    outline: str
    content: str
    evaluate: int

def create_outline(state: BlogState) -> BlogState:
    title = state['title']
    prompt = f'Generate a detailed outline for a blog on the title - {title}'
    outline = model.invoke(prompt).content
    state['outline'] = outline
    return state

def create_blog(state: BlogState) -> BlogState:
    title = state['title']
    outline = state['outline']
    prompt = f'Write a detailed blog on the title - {title} using the following outline \n {outline}'
    content = model.invoke(prompt).content
    state['content'] = content
    return state

def evaluate_blog_content(state: BlogState) -> BlogState:  # Renamed this function
    title = state['title']
    content = state['content']
    prompt = f"Evaluate ONLY the quality of this blog content and return JUST a single number between 0-10: Title:{title},Content:{content}"
    
    evaluation = model.invoke(prompt).content
    state['evaluation'] = evaluation
    return state

# Build the workflow graph
graph = StateGraph(BlogState)

graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_blog)
graph.add_node('evaluate_blog', evaluate_blog_content)  # Updated to use renamed function

graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', 'evaluate_blog')
graph.add_edge('evaluate_blog', END)

workflow = graph.compile()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_blog():
    try:
        data = request.get_json()
        title = data.get('title', 'Default Blog Title')
        
        generate_blog_initial_state = {'title': title}
        generate_blog_final_state = workflow.invoke(generate_blog_initial_state)
        
        return jsonify({
            'success': True,
            'title': title,
            'outline': generate_blog_final_state['outline'],
            'content': generate_blog_final_state['content']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@app.route('/evaluate', methods=['POST'])
def evaluate_blog():
    try:
        data = request.get_json()
        title = data.get('title', '')
        content = data.get('content', '')
        outline = data.get('outline', '')
        
        initial_state = {
            'title': title,
            'content': content,
            'outline': outline
        }
        
        # Call the renamed evaluation function
        final_state = evaluate_blog_content(initial_state)
        
        return jsonify({
            'success': True,
            'evaluation': final_state['evaluation']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)