import React, { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  name: string;
  text: string;
  timestamp: Date;
  isFlagged?: boolean;
  image?: string;
}

interface JeeResource {
  id: number;
  title: string;
  url: string;
  description: string;
}

interface StudyGroup {
  id: number;
  name: string;
  members: number;
  isJoined: boolean;
}

const PrepBoosterChat: React.FC = () => {
  // State management
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
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
  const [joinedGroups, setJoinedGroups] = useState<string[]>([]);
  
  const [jeeResources, setJeeResources] = useState<JeeResource[]>([
    { id: 1, title: 'JEE Main Previous Year Papers', url: '#', description: 'Download previous 10 years question papers' },
    { id: 2, title: 'NCERT Solutions', url: '#', description: 'Complete NCERT solutions for Physics, Chemistry, Math' },
    { id: 3, title: 'Important Formulas', url: '#', description: 'Quick revision formulas for all subjects' }
  ]);
  
  const [studyGroups, setStudyGroups] = useState<StudyGroup[]>([
    { id: 1, name: 'Physics Help Group', members: 23, isJoined: false },
    { id: 2, name: 'Chemistry Doubts', members: 18, isJoined: false },
    { id: 3, name: 'Math Problem Solving', members: 31, isJoined: false }
  ]);
  
  // Refs
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const adminPasswordRef = useRef('prepboosters0909');

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

  // Handle join/leave group
  const handleJoinGroup = (groupId: number) => {
    setStudyGroups(prev => prev.map(group => 
      group.id === groupId 
        ? { ...group, members: group.members + 1, isJoined: true }
        : group
    ));
    setJoinedGroups(prev => [...prev, `${groupId}`]);
    alert('Successfully joined the study group!');
  };

  const handleLeaveGroup = (groupId: number) => {
    setStudyGroups(prev => prev.map(group => 
      group.id === groupId 
        ? { ...group, members: Math.max(0, group.members - 1), isJoined: false }
        : group
    ));
    setJoinedGroups(prev => prev.filter(id => id !== `${groupId}`));
    alert('Left the study group successfully.');
  };

  // Check for blocked words
  const containsBlockedWord = (text: string) => {
    return blockedWords.some(word => 
      text.toLowerCase().includes(word.toLowerCase())
    );
  };

  // Handle image selection
  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert('Image size should be less than 5MB');
        return;
      }
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  // Remove selected image
  const removeImage = () => {
    setSelectedImage(null);
    setImagePreview('');
  };

  // Send message function
  const handleSendMessage = () => {
    if ((!currentMessage.trim() && !selectedImage) || bannedUsers.includes(userName.toLowerCase())) return;

    const messageContent = selectedImage ? 
      `📸 Image: ${currentMessage.trim() || 'Shared an image'}` : 
      currentMessage;

    if (containsBlockedWord(messageContent)) {
      const newMessage: Message = {
        id: Date.now().toString(),
        name: userName,
        text: messageContent,
        timestamp: new Date(),
        isFlagged: true,
        image: selectedImage ? imagePreview : undefined
      };

      setMessages(prev => [...prev, newMessage]);
      setFlaggedMessages(prev => [...prev, newMessage.id]);
      setCurrentMessage('');
      setSelectedImage(null);
      setImagePreview('');
      return;
    }

    const newMessage: Message = {
      id: Date.now().toString(),
      name: userName,
      text: messageContent,
      timestamp: new Date(),
      image: selectedImage ? imagePreview : undefined
    };

    setMessages(prev => [...prev, newMessage]);
    setCurrentMessage('');
    setSelectedImage(null);
    setImagePreview('');
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
                <span className="font-semibold text-green-600">{onlineUsers.length}</span>
              </div>
              <div className="flex justify-between">
                <span>Banned Users:</span>
                <span className="font-semibold">{bannedUsers.length}</span>
              </div>
              <div className="flex justify-between">
                <span>Active Groups:</span>
                <span className="font-semibold">{studyGroups.length}</span>
              </div>
            </div>

            <h4 className="font-semibold mt-4 mb-2 text-blue-600">System Info</h4>
            <div className="text-xs text-gray-600 space-y-1">
              <div>App Version: 2.0.0</div>
              <div>Last Updated: {new Date().toLocaleDateString()}</div>
              <div>Admin Access: Full Permissions</div>
            </div>
          </div>
        </div>

        {/* Advanced Controls */}
        <div className="bg-white p-4 rounded-lg shadow mt-4">
          <h4 className="font-semibold mb-3 text-blue-600">⚙️ Advanced Controls</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h5 className="font-medium mb-2">Message Management</h5>
              <div className="space-y-2 text-sm">
                <button 
                  onClick={() => setMessages(prev => prev.filter(msg => !msg.isFlagged))}
                  className="w-full bg-orange-500 text-white px-3 py-1 rounded hover:bg-orange-600"
                >
                  Remove All Flagged
                </button>
                <button 
                  onClick={() => setMessages([])}
                  className="w-full bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                >
                  Clear Chat History
                </button>
              </div>
            </div>
            <div>
              <h5 className="font-medium mb-2">User Controls</h5>
              <div className="space-y-2 text-sm">
                <button 
                  onClick={() => setOnlineUsers([])}
                  className="w-full bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                >
                  Kick All Users
                </button>
                <button 
                  onClick={() => setBannedUsers([])}
                  className="w-full bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                >
                  Unban All Users
                </button>
              </div>
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
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.极 01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 极 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                  </div>
                  <p>Start the conversation! Send your first message.</p>
                </div>
              ) : (
                messages.map((message) => (
                  <div key={message.id} className={`flex flex-col ${message.name === userName ? 'items-end' : ''}`}>
                    <div className="flex items-center space极 2 mb-1">
                      <span className="font-semibold text-indigo-600 text-sm">{message.name}</span>
                      <span className="text-xs text-gray-500">{formatTime(message.timestamp)}</span>
                      {message.isFlagged && (
                        <span className="text-xs bg-red-100 text-red-700 px-2 py-0.5 rounded">Flagged</span>
                      )}
                    </div>
                    <div className={`rounded-lg px-4 py-2 max-w-md ${message.name === userName ? 'bg-indigo-100' : 'bg-blue-50'} ${message.isFlagged ? 'border border-red-300' : ''}`}>
                      {message.image && (
                        <div className="mb-2">
                          <img 
                            src={message.image} 
                            alt="Shared content" 
                            className="rounded-lg max-w-full max-h-48 object-cover"
                          />
                        </div>
                      )}
                      <p className="text-gray-800 break-words">{message.text}</p>
                    </div>
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t p-4">
              {imagePreview && (
                <div className="mb-3 relative">
                  <img 
                    src={imagePreview} 
                    alt="Preview" 
                    className="rounded-lg max-h-32 object-cover"
                  />
                  <button
                    onClick={removeImage}
                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 text-xs"
                  >
                    ✕
                  </button>
                </div>
              )}
              <div className="flex space-x-3">
                <div className="flex-1 flex flex-col">
                  <input
                    type="text"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message or share an image..."
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent mb-2"
                    maxLength={500}
                  />
                  <label className="flex items-center text-sm text-indigo-600 cursor-pointer">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageSelect}
                      className="hidden"
                    />
                    <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Add Image
                  </label>
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={(!currentMessage.trim() && !selectedImage) || bannedUsers.includes(userName.toLowerCase())}
                  className="bg-indigo-极 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors self-end"
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
                <span className="text-green-500 mr-2">✓</span>
                <span>Help others with their doubts</span>
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
                  {group.isJoined ? (
                    <button 
                      onClick={() => handleLeaveGroup(group.id)}
                      className="bg-red-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-red-700"
                    >
                      Leave Group
                    </button>
                  ) : (
                    <button 
                      onClick={() => handleJoinGroup(group.id)}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700"
                    >
                      Join Group
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Admin Panel */}
      {renderAdminPanel()}

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