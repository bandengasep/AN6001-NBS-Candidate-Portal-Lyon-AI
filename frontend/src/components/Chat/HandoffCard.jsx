import { useState } from 'react';
import { Calendar, User, Mail, MessageSquare, CheckCircle } from 'lucide-react';

export function HandoffCard({ conversationId }) {
  const [formData, setFormData] = useState({ name: '', email: '', topic: '' });
  const [status, setStatus] = useState('form'); // 'form' | 'submitting' | 'success'
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.email.trim()) return;

    setStatus('submitting');
    setError(null);

    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';
      const res = await fetch(`${API_BASE_URL}/chat/handoff`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, conversation_id: conversationId || '' }),
      });

      if (!res.ok) throw new Error('Failed to submit');
      setStatus('success');
    } catch (err) {
      setError('Something went wrong. Please try again.');
      setStatus('form');
    }
  };

  if (status === 'success') {
    return (
      <div className="flex justify-start mb-3 message-enter">
        <div className="flex max-w-[85%] lg:max-w-[75%]">
          <div className="flex-shrink-0 mr-3">
            <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
              <CheckCircle className="h-4 w-4 text-green-600" />
            </div>
          </div>
          <div className="rounded-2xl rounded-bl-md px-5 py-4 bg-green-50 border border-green-200">
            <p className="text-sm text-green-800 font-medium">All set!</p>
            <p className="text-sm text-green-700 mt-1">
              An NBS advisor will reach out to you at <strong>{formData.email}</strong> shortly.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start mb-3 message-enter">
      <div className="flex max-w-[85%] lg:max-w-[75%]">
        <div className="flex-shrink-0 mr-3">
          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
            <Calendar className="h-4 w-4 text-blue-600" />
          </div>
        </div>
        <div className="rounded-2xl rounded-bl-md px-5 py-4 bg-white border border-gray-200 shadow-sm">
          <p className="text-sm font-medium text-gray-800 mb-3">
            Schedule a session with an NBS advisor
          </p>

          <form onSubmit={handleSubmit} className="space-y-3">
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Your name"
                required
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-nbs-red/20 focus:border-nbs-red"
              />
            </div>

            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="email"
                placeholder="Your email"
                required
                value={formData.email}
                onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-nbs-red/20 focus:border-nbs-red"
              />
            </div>

            <div className="relative">
              <MessageSquare className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <textarea
                placeholder="What would you like to discuss? (optional)"
                value={formData.topic}
                onChange={(e) => setFormData(prev => ({ ...prev, topic: e.target.value }))}
                rows={2}
                className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-nbs-red/20 focus:border-nbs-red resize-none"
              />
            </div>

            {error && (
              <p className="text-xs text-red-600">{error}</p>
            )}

            <button
              type="submit"
              disabled={status === 'submitting'}
              className="w-full py-2 text-sm font-medium text-white bg-nbs-red rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {status === 'submitting' ? 'Scheduling...' : 'Schedule Session'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default HandoffCard;
