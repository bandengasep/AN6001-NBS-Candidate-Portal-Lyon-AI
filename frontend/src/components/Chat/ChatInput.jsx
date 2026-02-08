import { useState, useRef, useEffect } from 'react';
import { Send, Trash2, Paperclip, X, FileText, Image } from 'lucide-react';
import { uploadChatFile } from '../../services/api';

const ACCEPTED_TYPES = '.pdf,.jpg,.jpeg,.png';

export function ChatInput({ onSend, onClear, isLoading, disabled }) {
  const [input, setInput] = useState('');
  const [attachedFile, setAttachedFile] = useState(null); // {file, extractedText, fileType, filename, status}
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`;
    }
  }, [input]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isLoading || disabled) return;

    // Need either text or a processed file
    const hasText = input.trim().length > 0;
    const hasFile = attachedFile?.status === 'ready';
    if (!hasText && !hasFile) return;

    let message = input.trim();
    if (hasFile) {
      const prefix = `[Attached file: ${attachedFile.filename}]\n\nExtracted content:\n${attachedFile.extractedText}\n\n`;
      message = prefix + (message || 'I uploaded this document. Can you review it?');
    }

    onSend(message);
    setInput('');
    setAttachedFile(null);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleFileSelect = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Reset file input so same file can be re-selected
    e.target.value = '';

    // Validate size
    if (file.size > 10 * 1024 * 1024) {
      setAttachedFile({ filename: file.name, status: 'error', error: 'File too large (max 10MB)' });
      return;
    }

    setAttachedFile({ filename: file.name, status: 'uploading' });

    try {
      const result = await uploadChatFile(file);
      setAttachedFile({
        filename: result.filename,
        extractedText: result.text,
        fileType: result.file_type,
        status: 'ready',
      });
    } catch (err) {
      setAttachedFile({
        filename: file.name,
        status: 'error',
        error: err.response?.data?.detail || 'Failed to process file',
      });
    }
  };

  const removeFile = () => {
    setAttachedFile(null);
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        {/* File attachment preview */}
        {attachedFile && (
          <div className={`mb-2 flex items-center gap-2 px-3 py-2 rounded-lg text-sm ${
            attachedFile.status === 'error'
              ? 'bg-red-50 text-red-700'
              : attachedFile.status === 'uploading'
              ? 'bg-yellow-50 text-yellow-700'
              : 'bg-blue-50 text-blue-700'
          }`}>
            {attachedFile.fileType === 'image'
              ? <Image className="h-4 w-4 flex-shrink-0" />
              : <FileText className="h-4 w-4 flex-shrink-0" />}

            <span className="flex-1 truncate">
              {attachedFile.status === 'uploading' && `Processing ${attachedFile.filename}...`}
              {attachedFile.status === 'ready' && `${attachedFile.filename} (ready)`}
              {attachedFile.status === 'error' && `${attachedFile.filename}: ${attachedFile.error}`}
            </span>

            {attachedFile.status === 'uploading' && (
              <div className="w-4 h-4 border-2 border-yellow-600 border-t-transparent rounded-full animate-spin flex-shrink-0" />
            )}

            <button type="button" onClick={removeFile} className="p-0.5 hover:bg-black/10 rounded flex-shrink-0">
              <X className="h-3.5 w-3.5" />
            </button>
          </div>
        )}

        <div className="flex items-end space-x-3">
          {/* Clear button */}
          <button
            type="button"
            onClick={onClear}
            className="flex-shrink-0 p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            title="Clear chat"
          >
            <Trash2 className="h-5 w-5" />
          </button>

          {/* File upload button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isLoading || disabled || attachedFile?.status === 'uploading'}
            className="flex-shrink-0 p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            title="Attach file (PDF, JPG, PNG)"
          >
            <Paperclip className="h-5 w-5" />
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept={ACCEPTED_TYPES}
            onChange={handleFileSelect}
            className="hidden"
          />

          {/* Input area */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={attachedFile?.status === 'ready'
                ? 'Add a message about your file, or press Enter to send...'
                : 'Ask me about NBS programmes...'}
              disabled={isLoading || disabled}
              rows={1}
              className="w-full resize-none rounded-xl border border-gray-300 px-4 py-3 pr-12 focus:border-nbs-red focus:ring-1 focus:ring-nbs-red outline-none disabled:bg-gray-50 disabled:cursor-not-allowed text-sm"
            />

            {/* Send button inside input */}
            <button
              type="submit"
              disabled={(!input.trim() && attachedFile?.status !== 'ready') || isLoading || disabled}
              className="absolute right-2 bottom-2 p-2 bg-nbs-red text-white rounded-lg hover:bg-nbs-red-dark disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Helper text */}
        <p className="text-xs text-gray-400 mt-2 text-center">
          Press Enter to send, Shift+Enter for new line | Attach PDF or images with the clip icon
        </p>
      </form>
    </div>
  );
}

export default ChatInput;
