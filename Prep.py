import React, { useState, useRef, useEffect } from 'react';

const PrepBoosterChat = () => {
  // State management
  const [messages, setMessages] = useState<Array<{id: string, name: string, text: string, timestamp: Date, isFlagged?: boolean}>>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [userName, setUserName] = useState('');
  const [isNameSet, setIsNameSet] = useState(false);
  const [adminMode, setAdminMode] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [flaggedMessages, setFlaggedMessages] = useState<string[]>([]);
  const [bannedUsers, setBannedUsers] = useState<string[]>([]);
  const [onlineUsers, setOnlineUsers] = useState<string[]>([]);
  const [showOnlineUsers, setShowOnlineUsers] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [jeeResources, setJeeResources] = useState([
    { id: 1, title: 'JEE Main Previous Year Papers', url: '#', description: 'Download previous 10 years question papers' },
    { id: 2, title: 'NCERT Solutions', url: '#', description: 'Complete NCERT solutions for Physics, Chemistry, Math' },
    { id: 3, title: 'Important Formulas', url: '#', description: 'Quick revision formulas for all subjects' }
  ]);
  const [studyGroups, setStudyGroups] = useState([
    { id: 1, name: 'Physics Help Group', members: 23 },
    { id: 2, name: 'Chemistry Doubts', members: 18 },
    { id: 3, name: 'Math Problem Solving', members: 31 }
  ]);
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const adminPasswordRef = useRef('prepboosters0909'); // Default admin password

  // Blocked words list
  const blockedWords = ['gaali', 'abuse', 'curse', 'fuck', 'shit', 'asshole', 'bastard', 'mc', 'bc', 'chod'];

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle user name setup
  const handleSetName = () => {
    if (userName.trim() && !bannedUsers.includes(userName.toLowerCase())) {
      setIsNameSet(true);
      setOnlineUsers(prev => [...prev, userName]);
    } else if (bannedUsers.includes(userName.toLowerCase())) {
      alert('This username has been banned. Please choose a different name.');
    }
  };

  // Check for blocked words
  const containsBlockedWord = (text: string) => {
    return blockedWords.some(word => 
      text.toLowerCase().includes(word.toLowerCase())
    );
  };

  // Send message function
  const handleSendMessage = () => {
    if (!currentMessage.trim() || bannedUsers.includes(userName.toLowerCase())) return;

    if (containsBlockedWord(currentMessage)) {
      const newMessage = {
        id: Date.now().toString(),
        name: userName,
        text: currentMessage,
        timestamp: new Date(),
        isFlagged: true
      };

      setMessages(prev => [...prev, newMessage]);
      setFlaggedMessages(prev => [...prev, newMessage.id]);
      setCurrentMessage('');
      return;
    }

    const newMessage = {
      id: Date.now().toString(),
      name: userName,
      text: currentMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newMessage]);
    setCurrentMessage('');
  };

  // Handle key press for sending messages
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Admin login function
  const handleAdminLogin = () => {
    if (adminPassword === adminPasswordRef.current) {
      setAdminMode(true);
      setShowAdminLogin(false);
      alert('Admin access granted');
    } else {
      alert('Incorrect admin password');
    }
    setAdminPassword('');
  };

  // Format time for messages
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Admin functions
  const deleteMessage = (id: string) => {
    setMessages(prev => prev.filter(msg => msg.id !== id));
  };

  const banUser = (name: string) => {
    if (!bannedUsers.includes(name.toLowerCase())) {
      setBannedUsers(prev => [...prev, name.toLowerCase()]);
      setOnlineUsers(prev => prev.filter(user => user !== name));
      alert(`User ${name} has been banned`);
    }
  };

  const unbanUser = (name: string) => {
    setBannedUsers(prev => prev.filter(user => user !== name.toLowerCase()));
    alert(`User ${name} has been unbanned`);
  };

  const clearFlaggedMessages = () => {
    setMessages(prev => prev.filter(msg => !msg.isFlagged));
    setFlaggedMessages([]);
  };

  // Render admin panel
  const renderAdminPanel = () => {
    if (!adminMode) return null;

    return (
      <div className="bg-gray-100 border-t p-4">
        <h3 className="font-bold text-lg mb-3 text-red-600">Admin Panel</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="font-semibold mb-2">Flagged Messages ({flaggedMessages.length})</h4>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {messages.filter(msg => msg.isFlagged).map(msg => (
                <div key={msg.id} className="bg-red-100 p-2 rounded text-sm">
                  <div className="flex justify-between">
                    <span className="font-medium">{msg.name}:</span>
                    <span>{formatTime(msg.timestamp)}</span>
                  </div>
                  <p className="mt-1">{msg.text}</p>
                  <div className="flex space-x-2 mt-2">
                    <button 
                      onClick={() => deleteMessage(msg.id)}
                      className="text-xs bg-red-500 text-white px-2 py-1 rounded"
                    >
                      Delete
                    </button>
                    <button 
                      onClick={() => banUser(msg.name)}
                      className="text-xs bg-red-700 text-white px-2 py-1 rounded"
                    >
                      Ban User
                    </button>
                  </div>
                </div>
              ))}
            </div>
            {flaggedMessages.length > 0 && (
              <button 
                onClick={clearFlaggedMessages}
                className="mt-2 bg-red-600 text-white px-3 py-1 rounded text-sm"
              >
                Clear All Flagged
              </button>
            )}
          </div>
          
          <div>
            <h4 className="font-semibold mb-2">Banned Users ({bannedUsers.length})</h4>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {bannedUsers.map((user, index) => (
                <div key={index} className="bg-gray-200 p-2 rounded text-sm flex justify-between items-center">
                  <span>{user}</span>
                  <button 
                    onClick={() => unbanUser(user)}
                    className="bg-green-500 text-white px-2 py-1 rounded text-xs"
                  >
                    Unban
                  </button>
                </div>
              ))}
            </div>
            
            <h4 className="font-semibold mt-4 mb-2">Online Users ({onlineUsers.length})</h4>
            <div className="space-y-1 max-h-40 overflow-y-auto">
              {onlineUsers.map((user, index) => (
                <div key={index} className="bg-blue-100 p-2 rounded text-sm flex justify-between items-center">
                  <span>{user}</span>
                  <button 
                    onClick={() => banUser(user)}
                    className="bg-red-500 text-white px-2 py-1 rounded text-xs"
                  >
                    Ban
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Name input screen
  if (!isNameSet) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-indigo-600 mb-2">PrepBooster</h1>
            <p className="text-gray-600">Your preparation partner</p>
          </div>
          
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                Enter your name to join the JEE prep community
              </label>
              <input
                id="name"
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Your name"
                maxLength={50}
              />
            </div>
            
            <button
              onClick={handleSetName}
              disabled={!userName.trim()}
              className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Join JEE Prep Community
            </button>
            
            <div className="text-center text-sm text-gray-600">
              Get help with Physics, Chemistry & Math doubts from fellow aspirants
            </div>
            
            <button
              onClick={() => setShowAdminLogin(true)}
              className="w-full text-indigo-600 py-2 px-4 rounded-lg hover:bg-indigo-50 transition-colors border border-indigo-200"
            >
              Admin Login
            </button>
          </div>
          
          {showAdminLogin && (
            <div className="mt-6 p-4 bg-gray-100 rounded-lg">
              <h3 className="font-semibold mb-2">Admin Login</h3>
              <input
                type="password"
                value={adminPassword}
                onChange={(e) => setAdminPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded mb-2"
                placeholder="Admin password"
              />
              <div className="flex space-x-2">
                <button
                  onClick={handleAdminLogin}
                  className="flex-1 bg-red-600 text-white py-2 px-4 rounded"
                >
                  Login
                </button>
                <button
                  onClick={() => setShowAdminLogin(false)}
                  className="flex-1 bg-gray-500 text-white py-2 px-4 rounded"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Main chat interface
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">PB</span>
              </div>
              <h1 className="text-xl font-bold text-indigo-600">PrepBooster</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, {userName}</span>
              <div className="flex space-x-2">
                <button
                  onClick={() => setShowOnlineUsers(!showOnlineUsers)}
                  className="text-sm text-indigo-600 hover:text-indigo-800 flex items-center"
                >
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                  {onlineUsers.length} Online
                </button>
                <button
                  onClick={() => setIsNameSet(false)}
                  className="text-sm text-indigo-600 hover:text-indigo-800"
                >
                  Change Name
                </button>
                {!adminMode && (
                  <button
                    onClick={() => setShowAdminLogin(true)}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Admin
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Online Users Panel */}
      {showOnlineUsers && (
        <div className="bg-white border-b shadow-sm">
          <div className="max-w-6xl mx-auto px-4 py-3">
            <div className="flex justify-between items-center mb-2">
              <h3 className="font-semibold">Online Users</h3>
              <button onClick={() => setShowOnlineUsers(false)} className="text-gray-500">
                ✕
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {onlineUsers.map((user, index) => (
                <span key={index} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                  {user}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="font-semibold text-lg mb-4">Admin Login</h3>
            <input
              type="password"
              value={adminPassword}
              onChange={(e) => setAdminPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-4"
              placeholder="Enter admin password"
            />
            <div className="flex space-x-3">
              <button
                onClick={handleAdminLogin}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded-lg"
              >
                Login
              </button>
              <button
                onClick={() => setShowAdminLogin(false)}
                className="flex-1 bg-gray-500 text-white py-2 px-4 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 py-6">
        {/* Tabs Navigation */}
        <div className="flex border-b border-gray-200 mb-6">
          <button
            onClick={() => setActiveTab('chat')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'chat'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Study Chat
          </button>
          <button
            onClick={() => setActiveTab('resources')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'resources'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            JEE Resources
          </button>
          <button
            onClick={() => setActiveTab('groups')}
            className={`px-4 py-2 font-medium ${
              activeTab === 'groups'
                ? 'border-b-2 border-indigo-600 text-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            Study Groups
          </button>
        </div>

        {activeTab === 'chat' && (
        <div className="flex flex-col md:flex-row gap-6">
          {/* Chat Container */}
          <div className="bg-white rounded-lg shadow-lg flex-1 flex flex-col">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 py-8">
                <div className="w-16 h-16 mx-auto mb-4 bg-indigo-100 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <p>Start the conversation! Send your first message.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div key={message.id} className={`flex flex-col ${message.name === userName ? 'items-end' : ''}`}>
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-semibold text-indigo-600 text-sm">{message.name}</span>
                    <span className="text-xs text-gray-500">{formatTime(message.timestamp)}</span>
                    {message.isFlagged && (
                      <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">Flagged</span>
                    )}
                  </div>
                  <div className={`rounded-lg px-4 py-2 max-w-xs ${message.name === userName ? 'bg-indigo-100' : 'bg-blue-50'} ${message.isFlagged ? 'border border-red-300' : ''}`}>
                    <p className="text-gray-800">{message.text}</p>
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t p-4">
            <div className="flex space-x-3">
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                maxLength={500}
              />
              <button
                onClick={handleSendMessage}
                disabled={!currentMessage.trim() || bannedUsers.includes(userName.toLowerCase())}
                className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Send
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              {bannedUsers.includes(userName.toLowerCase()) 
                ? 'Your account has been banned from sending messages.'
                : 'Messages containing inappropriate content will be flagged automatically.'
              }
            </p>
          </div>
        </div>

        {/* Info Panel */}
        <div className="bg-white rounded-lg shadow-lg p-6 w-full md:w-80">
          <h2 className="font-bold text-lg mb-4 text-indigo-600">JEE Prep Guidelines</h2>
          <ul className="space-y-3 text-sm">
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Ask specific doubts with question details</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Share useful study resources and tips</span>
            </li>
            <li className="flex items-start">
              <span className="text-red-500 mr-2">✗</span>
              <span>No abusive language or harassment</span>
            </li>
            <li className="flex items-start">
              <span className="text-red-500 mr-2">✗</span>
              <span>No sharing of irrelevant content</span>
            </li>
          </ul>
          
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold mb-2">JEE Help Resources</h3>
            <p className="text-sm text-gray-600">
              Get study materials at: <span className="text-indigo-600">resources@prepbooster.com</span>
            </p>
          </div>
          
          {adminMode && (
            <div className="mt-6 p-4 bg-red-50 rounded-lg">
              <h3 className="font-semibold mb-2 text-red-700">Admin Mode Active</h3>
              <p className="text-sm text-red-600">
                You have full administrative control over the chat.
              </p>
              <button
                onClick={() => setAdminMode(false)}
                className="mt-2 text-sm text-red-700 underline"
              >
                Exit Admin Mode
              </button>
            </div>
          )}
        </div>
      </div>
      )}

      {/* JEE Resources Tab */}
      {activeTab === 'resources' && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="font-bold text-2xl mb-6 text-indigo-600">JEE Preparation Resources</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jeeResources.map(resource => (
              <div key={resource.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-lg mb-2 text-indigo-700">{resource.title}</h3>
                <p className="text-gray-600 text-sm mb-3">{resource.description}</p>
                <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-indigo-700">
                  Download
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Study Groups Tab */}
      {activeTab === 'groups' && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="font-bold text-2xl mb-6 text-indigo-600">Study Groups</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {studyGroups.map(group => (
              <div key={group.id} className="border rounded-lg p-4">
                <h3 className="font-semibold text-lg mb-2">{group.name}</h3>
                <p className="text-gray-600 text-sm mb-3">{group.members} members active</p>
                <button className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700">
                  Join Group
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>

      {/* Admin Panel */}
      {adminMode && renderAdminPanel()}

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <p className="text-center text-sm text-gray-600">
            © 2024 PrepBooster - Safe and productive learning environment
          </p>
        </div>
      </footer>
    </div>
  );
};

export default PrepBoosterChat;
