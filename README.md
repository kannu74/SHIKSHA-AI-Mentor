<h1>Shiksha AI Mentor</h1>

<h3>Description</h3>
<p>Shiksha AI is an intelligent academic assistant designed to help students better understand NCERT concepts. It is powered by a fine-tuned LLaMA model to provide natural, human-like answers to curriculum-based questions. The project features two different training phases: one based solely on NCERT datasets and another that incorporates human-like conversational data to improve response quality. It includes user authentication, MongoDB-based logging, and a complete front-end interface built with Streamlit.</p>

<h3>Finetuned Models</h3>
<ul>
  <li><strong>Model 1</strong>: <code>lora_mentor_model</code> (with <code>lora_mentor_model_tokenizer</code>) - Fine-tuned on NCERT datasets only.</li>
  <li><strong>Model 2</strong>: <code>lora_mentor_modelv2</code> (with <code>lora_mentor_model_tokenizerv2</code>) - Fine-tuned on both NCERT and human-like datasets using LoRA PEFT (Parameter Efficient Fine-Tuning).</li>
</ul>

<h3>Datasets Used</h3>
<ul>
  <li>NCERT Datasets:
    <ul>
      <li>Physics, Chemistry, and Biology (Class 11 & 12)</li>
      <li>Psychology (Class 11 & 12)</li>
      <li>Science (Class 10)</li>
    </ul>
  </li>
  <li>Human-like Datasets:
    <ul>
      <li><code>databricks-dolly-15k</code></li>
      <li><code>sharegpt-english</code></li>
    </ul>
  </li>
</ul>

<h3>Preprocessing & Fine-Tuning</h3>
<ul>
  <li><strong>ncert_12th_preprocessing.ipynb</strong>: Preprocesses Class 12 NCERT data</li>
  <li><strong>human_finetuning/human_dataset_preprocessing.ipynb</strong>: Preprocesses human-like datasets</li>
  <li><strong>llama_finetuning_v2.ipynb</strong>: Fine-tunes the TinyLlama model using LoRA</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Framework: FastAPI</li>
  <li>Authentication: Student login/signup using hashed passwords (bcrypt)</li>
  <li>Database: MongoDB for user data and session logs</li>
  <li>Key API endpoints:
    <ul>
      <li><code>/signup/</code>: Create new account</li>
      <li><code>/login/</code>: User authentication</li>
      <li><code>/ask_question/</code>: Ask a question with logged <code>student_id</code></li>
    </ul>
  </li>
</ul>

<h3>Frontend</h3>
<ul>
  <li>Framework: Streamlit</li>
  <li>Functionalities:
    <ul>
      <li>Login & account creation</li>
      <li>Ask subject-related questions</li>
      <li>Receive human-like, accurate answers from the LLaMA model</li>
    </ul>
  </li>
</ul>

<h3>How to Run Locally</h3>
<ol>
  <li>Clone the repository:
    <pre><code>git clone &lt;repo-url&gt;</code></pre>
  </li>
  <li>Install Python dependencies:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Start MongoDB locally or connect to a remote MongoDB instance.</li>
  <li>Run the FastAPI backend:
    <pre><code>uvicorn backend:app --reload</code></pre>
  </li>
  <li>In another terminal, run the Streamlit frontend:
    <pre><code>streamlit run app.py</code></pre>
  </li>
</ol>

<h3>Future Improvements</h3>
<ul>
  <li>Student progress tracking</li>
  <li>Teacher dashboard for performance analysis</li>
  <li>Voice interaction support</li>
</ul>

<h3>Acknowledgments</h3>
<ul>
  <li><code>TinyLlama/TinyLlama-1.1B-Chat-v1.0</code> from HuggingFace</li>
  <li>Datasets by <code>KadamParth</code>, <code>databricks</code>, and <code>theblackcat102</code></li>
</ul>
