/**
 * 中国古代教育史问答机器人 - 前端脚本
 */

// API基础URL
const API_BASE = '/api';

// 当前会话ID
let currentSessionId = generateSessionId();

// 当前对话标题
let currentChatTitle = '新对话';

// 选中的PDF文件
let selectedFile = null;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    loadConversationHistory();
    setupEventListeners();
});

// 生成会话ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// 设置事件监听
function setupEventListeners() {
    const sendButton = document.getElementById('sendButton');
    const messageInput = document.getElementById('messageInput');

    messageInput.addEventListener('input', () => {
        sendButton.disabled = !messageInput.value.trim();
    });

    // 初始禁用发送按钮
    sendButton.disabled = true;
}

// 检查健康状态
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            updateStatus(true, '已连接');
        } else {
            updateStatus(false, '连接异常');
        }
    } catch (error) {
        updateStatus(false, '连接失败');
    }
}

// 更新系统状态
function updateStatus(connected, text) {
    const indicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');

    if (connected) {
        indicator.classList.remove('bg-red-500');
        indicator.classList.add('bg-green-500');
    } else {
        indicator.classList.remove('bg-green-500');
        indicator.classList.add('bg-red-500');
    }
    statusText.textContent = text;
}

// 发送消息
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const question = messageInput.value.trim();

    if (!question) return;

    // 显示用户消息
    addMessage('user', question);

    // 清空输入框
    messageInput.value = '';
    document.getElementById('sendButton').disabled = true;

    // 如果是新对话的第一个消息，更新标题
    if (currentChatTitle === '新对话') {
        currentChatTitle = question.substring(0, 20) + (question.length > 20 ? '...' : '');
        document.getElementById('chatTitle').textContent = currentChatTitle;
        saveConversationToHistory();
    }

    // 显示加载状态
    const loadingId = addLoadingMessage();

    try {
        const response = await fetch(`${API_BASE}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                session_id: currentSessionId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // 移除加载消息
        removeLoadingMessage(loadingId);

        // 显示回答
        addMessage('assistant', data.answer, data.sources);

        // 更新对话历史
        loadConversationHistory();

    } catch (error) {
        removeLoadingMessage(loadingId);
        addMessage('assistant', `抱歉，回答问题时出现错误：${error.message}`, []);
        console.error('Error:', error);
    }
}

// 添加消息到聊天区域
function addMessage(role, content, sources = []) {
    const messagesContainer = document.getElementById('messagesContainer');

    // 移除欢迎消息（如果存在）
    const welcomeMessage = messagesContainer.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'} mb-6 message-bubble`;

    const messageContent = `
        <div class="${role === 'user' ? 'bg-blue-600 text-white' : 'bg-white text-gray-800'} rounded-2xl px-6 py-4 max-w-3xl shadow-md">
            <div class="prose ${role === 'user' ? 'prose-invert' : ''}">
                ${formatMessage(content)}
            </div>
            ${sources.length > 0 ? `
                <div class="mt-3 pt-3 border-t ${role === 'user' ? 'border-blue-400' : 'border-gray-200'}">
                    <div class="text-xs ${role === 'user' ? 'text-blue-200' : 'text-gray-500'} mb-2">
                        <i class="fas fa-book mr-1"></i>参考来源
                    </div>
                    ${sources.map(source => `
                        <div class="source-tag inline-block text-white text-xs px-2 py-1 rounded-full mr-2 mb-2">
                            ${source}
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        </div>
    `;

    messageDiv.innerHTML = messageContent;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    return messageDiv;
}

// 格式化消息内容
function formatMessage(content) {
    // 简单的Markdown格式转换
    return content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // 粗体
        .replace(/\*(.*?)\*/g, '<em>$1</em>')              // 斜体
        .replace(/`(.*?)`/g, '<code class="bg-gray-100 px-1 rounded">$1</code>')  // 行内代码
        .replace(/\n/g, '<br>');                             // 换行
}

// 添加加载消息
function addLoadingMessage() {
    const messagesContainer = document.getElementById('messagesContainer');
    const loadingId = 'loading_' + Date.now();

    const loadingDiv = document.createElement('div');
    loadingDiv.id = loadingId;
    loadingDiv.className = 'flex justify-start mb-6';
    loadingDiv.innerHTML = `
        <div class="bg-white rounded-2xl px-6 py-4 shadow-md">
            <div class="flex items-center gap-2 text-gray-500">
                <div class="animate-bounce">●</div>
                <div class="animate-bounce" style="animation-delay: 0.1s">●</div>
                <div class="animate-bounce" style="animation-delay: 0.2s">●</div>
            </div>
        </div>
    `;

    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    return loadingId;
}

// 移除加载消息
function removeLoadingMessage(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

// 键盘事件处理
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 创建新对话
function createNewChat() {
    currentSessionId = generateSessionId();
    currentChatTitle = '新对话';
    document.getElementById('chatTitle').textContent = currentChatTitle;

    // 清空消息区域
    const messagesContainer = document.getElementById('messagesContainer');
    messagesContainer.innerHTML = `
        <div class="flex justify-center mb-8 welcome-message">
            <div class="bg-white rounded-xl shadow-lg p-8 max-w-2xl">
                <div class="text-center mb-6">
                    <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-graduation-cap text-blue-600 text-2xl"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-2">开始新对话</h3>
                    <p class="text-gray-600">我是您的专业考研辅导老师，专注于中国古代教育史领域</p>
                </div>
                <div class="bg-blue-50 rounded-lg p-4">
                    <p class="text-sm text-blue-700">
                        <i class="fas fa-lightbulb mr-2"></i>
                        您可以询问关于中国古代教育史的各种问题，如教育制度、教育思想、科举制度等。
                    </p>
                </div>
            </div>
        </div>
    `;

    saveConversationToHistory();
}

// 加载对话历史
async function loadConversationHistory() {
    try {
        const response = await fetch(`${API_BASE}/sessions`);
        if (response.ok) {
            const data = await response.json();
            updateConversationList(data.sessions);
        }
    } catch (error) {
        console.error('加载对话历史失败:', error);
    }
}

// 更新对话列表
function updateConversationList(sessions) {
    const conversationList = document.getElementById('conversationList');

    if (sessions.length === 0) {
        conversationList.innerHTML = `
            <div class="text-center text-gray-400 py-4">
                <i class="fas fa-inbox mb-2"></i>
                <p class="text-sm">暂无历史对话</p>
            </div>
        `;
        return;
    }

    conversationList.innerHTML = sessions.map(sessionId => `
        <div
            class="flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer hover:bg-blue-700 transition duration-200 group"
            onclick="switchConversation('${sessionId}')"
        >
            <div class="flex items-center gap-2 overflow-hidden">
                <i class="fas fa-comment text-blue-200"></i>
                <span class="truncate text-sm">${sessionId === currentSessionId ? currentChatTitle : '历史对话'}</span>
            </div>
            <button
                onclick="event.stopPropagation(); deleteConversation('${sessionId}')"
                class="text-blue-200 hover:text-white opacity-0 group-hover:opacity-100 transition duration-200"
            >
                <i class="fas fa-trash text-xs"></i>
            </button>
        </div>
    `).join('');
}

// 切换对话
async function switchConversation(sessionId) {
    if (sessionId === currentSessionId) return;

    currentSessionId = sessionId;

    // 获取对话历史
    try {
        const response = await fetch(`${API_BASE}/history/${sessionId}`);
        if (response.ok) {
            const data = await response.json();

            // 清空消息区域
            const messagesContainer = document.getElementById('messagesContainer');
            messagesContainer.innerHTML = '';

            // 显示历史消息
            data.messages.forEach(msg => {
                addMessage(msg.role, msg.content, []);
            });

            // 更新标题
            if (data.messages.length > 0) {
                const firstUserMsg = data.messages.find(m => m.role === 'user');
                if (firstUserMsg) {
                    currentChatTitle = firstUserMsg.content.substring(0, 20) +
                        (firstUserMsg.content.length > 20 ? '...' : '');
                }
            } else {
                currentChatTitle = '新对话';
            }
            document.getElementById('chatTitle').textContent = currentChatTitle;
        }
    } catch (error) {
        console.error('加载对话失败:', error);
        showNotification('加载对话失败', 'error');
    }
}

// 删除对话
async function deleteConversation(sessionId) {
    if (!confirm('确定要删除这个对话吗？')) return;

    try {
        const response = await fetch(`${API_BASE}/history/${sessionId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            if (sessionId === currentSessionId) {
                createNewChat();
            }
            loadConversationHistory();
            showNotification('对话已删除', 'success');
        }
    } catch (error) {
        console.error('删除对话失败:', error);
        showNotification('删除对话失败', 'error');
    }
}

// 保存对话到历史
function saveConversationToHistory() {
    loadConversationHistory();
}

// 显示上传模态框
function showUploadModal() {
    document.getElementById('uploadModal').classList.remove('hidden');
    document.getElementById('uploadModal').classList.add('flex');
    selectedFile = null;
    document.getElementById('uploadStatus').textContent = '';
    document.getElementById('uploadButton').disabled = true;
}

// 隐藏上传模态框
function hideUploadModal() {
    document.getElementById('uploadModal').classList.add('hidden');
    document.getElementById('uploadModal').classList.remove('flex');
}

// 拖拽处理
function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('border-blue-500', 'bg-blue-50');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');
}

function handleDrop(event) {
    event.preventDefault();
    event.currentTarget.classList.remove('border-blue-500', 'bg-blue-50');

    const files = event.dataTransfer.files;
    if (files.length > 0) {
        selectFile(files[0]);
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        selectFile(file);
    }
}

function selectFile(file) {
    if (!file.name.endsWith('.pdf')) {
        showNotification('请选择PDF文件', 'error');
        return;
    }

    selectedFile = file;
    document.getElementById('uploadStatus').innerHTML = `
        <div class="flex items-center gap-2 text-green-600">
            <i class="fas fa-check-circle"></i>
            <span>${file.name} (${formatFileSize(file.size)})</span>
        </div>
    `;
    document.getElementById('uploadButton').disabled = false;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// 上传PDF
async function uploadPDF() {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch(`${API_BASE}/upload-pdf`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            showNotification(`PDF上传成功：${data.filename}`, 'success');
            hideUploadModal();
        } else {
            throw new Error('上传失败');
        }
    } catch (error) {
        console.error('上传失败:', error);
        showNotification('PDF上传失败', 'error');
    }
}

// 显示PDF列表
function showPDFList() {
    const modal = document.getElementById('pdfListModal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');

    loadPDFList();
}

function hidePDFList() {
    const modal = document.getElementById('pdfListModal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

// 加载PDF列表
async function loadPDFList() {
    try {
        const response = await fetch(`${API_BASE}/pdfs`);
        if (response.ok) {
            const data = await response.json();
            renderPDFList(data.pdfs);
        }
    } catch (error) {
        console.error('加载PDF列表失败:', error);
        document.getElementById('pdfList').innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-exclamation-circle text-3xl mb-2"></i>
                <p>加载失败</p>
            </div>
        `;
    }
}

// 渲染PDF列表
function renderPDFList(pdfs) {
    const pdfListContainer = document.getElementById('pdfList');

    if (pdfs.length === 0) {
        pdfListContainer.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <i class="fas fa-folder-open text-3xl mb-2"></i>
                <p>暂无PDF文件</p>
                <p class="text-sm mt-2">请上传知识库文件</p>
            </div>
        `;
        return;
    }

    pdfListContainer.innerHTML = pdfs.map(pdf => `
        <div class="bg-gray-50 rounded-lg p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                    <i class="fas fa-file-pdf text-red-500"></i>
                </div>
                <div>
                    <div class="font-medium text-gray-800">${pdf}</div>
                    <div class="text-sm text-gray-500">PDF文件</div>
                </div>
            </div>
            <button
                onclick="deletePDF('${pdf}')"
                class="text-red-500 hover:text-red-700 transition duration-200 p-2"
                title="删除文件"
            >
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');
}

// 删除PDF
async function deletePDF(filename) {
    if (!confirm(`确定要删除 ${filename} 吗？`)) return;

    try {
        const response = await fetch(`${API_BASE}/pdfs/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification(`文件 ${filename} 已删除`, 'success');
            loadPDFList();
        } else {
            throw new Error('删除失败');
        }
    } catch (error) {
        console.error('删除失败:', error);
        showNotification('删除PDF失败', 'error');
    }
}

// 初始化知识库
async function initKnowledgeBase() {
    if (!confirm('确定要初始化知识库吗？这将从所有PDF文件构建向量索引，可能需要一些时间。')) {
        return;
    }

    showNotification('正在初始化知识库，请稍候...', 'info');

    try {
        const response = await fetch(`${API_BASE}/init-knowledge-base`, {
            method: 'POST'
        });

        if (response.ok) {
            const data = await response.json();
            showNotification(`知识库初始化成功！已处理 ${data.document_count} 个文档片段`, 'success');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.detail || '初始化失败');
        }
    } catch (error) {
        console.error('初始化知识库失败:', error);
        showNotification(`初始化失败：${error.message}`, 'error');
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    const notificationText = document.getElementById('notificationText');
    const notificationIcon = document.getElementById('notificationIcon');

    notificationText.textContent = message;

    // 设置图标和颜色
    switch (type) {
        case 'success':
            notificationIcon.className = 'fas fa-check-circle text-green-500';
            break;
        case 'error':
            notificationIcon.className = 'fas fa-exclamation-circle text-red-500';
            break;
        case 'warning':
            notificationIcon.className = 'fas fa-exclamation-triangle text-yellow-500';
            break;
        default:
            notificationIcon.className = 'fas fa-info-circle text-blue-500';
    }

    notification.classList.remove('hidden');

    // 3秒后自动隐藏
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}
