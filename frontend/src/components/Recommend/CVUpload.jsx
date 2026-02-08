import { useState, useRef } from 'react';
import { parseCV } from '../../services/api';

/**
 * CV Upload step with drag-and-drop and skip option.
 * @param {Object} props
 * @param {Function} props.onParsed - Called with parsed CV data
 * @param {Function} props.onSkip - Called when user skips CV upload
 */
export function CVUpload({ onParsed, onSkip }) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const [parsed, setParsed] = useState(null);
  const fileRef = useRef(null);

  async function handleFile(file) {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please upload a PDF file.');
      return;
    }

    setError(null);
    setIsUploading(true);

    try {
      const data = await parseCV(file);
      setParsed(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to parse CV. Please try again or skip.');
    } finally {
      setIsUploading(false);
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  }

  function handleDragOver(e) {
    e.preventDefault();
    setIsDragging(true);
  }

  if (parsed) {
    return (
      <div>
        <h2 className="text-xl font-bold text-ntu-dark mb-4">CV Parsed Successfully</h2>
        <div className="bg-white border border-ntu-border rounded-lg p-5 space-y-3 mb-6">
          {parsed.education_level && (
            <div className="flex justify-between text-sm">
              <span className="text-ntu-muted">Education</span>
              <span className="text-ntu-dark font-medium">{parsed.education_level}</span>
            </div>
          )}
          {parsed.years_experience != null && (
            <div className="flex justify-between text-sm">
              <span className="text-ntu-muted">Experience</span>
              <span className="text-ntu-dark font-medium">{parsed.years_experience} years</span>
            </div>
          )}
          {parsed.industry && (
            <div className="flex justify-between text-sm">
              <span className="text-ntu-muted">Industry</span>
              <span className="text-ntu-dark font-medium">{parsed.industry}</span>
            </div>
          )}
          {parsed.quantitative_background && (
            <div className="flex justify-between text-sm">
              <span className="text-ntu-muted">Quantitative</span>
              <span className="text-ntu-dark font-medium">{parsed.quantitative_background}</span>
            </div>
          )}
          {parsed.leadership_experience && (
            <div className="flex justify-between text-sm">
              <span className="text-ntu-muted">Leadership</span>
              <span className="text-ntu-dark font-medium">{parsed.leadership_experience}</span>
            </div>
          )}
          {parsed.skills?.length > 0 && (
            <div>
              <span className="text-ntu-muted text-sm block mb-1">Skills</span>
              <div className="flex flex-wrap gap-1.5">
                {parsed.skills.map((s) => (
                  <span key={s} className="text-xs bg-ntu-red/[0.08] text-ntu-red px-2 py-0.5 rounded">{s}</span>
                ))}
              </div>
            </div>
          )}
        </div>
        <div className="flex gap-3">
          <button onClick={() => onParsed(parsed)}
                  className="px-6 py-2.5 bg-ntu-red text-white rounded font-semibold text-sm hover:bg-ntu-red-hover transition-colors">
            Continue with this CV
          </button>
          <button onClick={() => { setParsed(null); setError(null); }}
                  className="px-6 py-2.5 border border-ntu-border text-ntu-body rounded text-sm hover:border-ntu-red hover:text-ntu-red transition-colors">
            Upload different CV
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-xl font-bold text-ntu-dark mb-2">Upload Your CV</h2>
      <p className="text-sm text-ntu-muted mb-6">
        We'll extract your background to pre-fill quiz answers. This step is optional.
      </p>

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={() => setIsDragging(false)}
        onClick={() => fileRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
          isDragging ? 'border-ntu-red bg-ntu-red/[0.04]' : 'border-ntu-border hover:border-ntu-red/50'
        }`}
      >
        <input
          ref={fileRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />
        {isUploading ? (
          <div className="space-y-2">
            <div className="w-8 h-8 border-2 border-ntu-red border-t-transparent rounded-full animate-spin mx-auto" />
            <p className="text-sm text-ntu-muted">Parsing your CV...</p>
          </div>
        ) : (
          <>
            <svg className="w-10 h-10 text-ntu-muted mx-auto mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/><path d="M12 18v-6"/><path d="M9 15l3-3 3 3"/>
            </svg>
            <p className="text-sm text-ntu-body font-medium">Drag & drop your CV here or click to browse</p>
            <p className="text-xs text-ntu-muted mt-1">PDF files only</p>
          </>
        )}
      </div>

      {error && <p className="text-sm text-red-600 mt-3">{error}</p>}

      <button onClick={onSkip}
              className="mt-6 text-sm text-ntu-muted hover:text-ntu-red transition-colors underline">
        Skip this step and go to quiz
      </button>
    </div>
  );
}
