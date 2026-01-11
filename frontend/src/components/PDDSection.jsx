import { useState } from 'react'
import axios from 'axios'
import DOMPurify from 'dompurify'
import config from '../config'
import './PDDSection.css'

function PDDSection({ section, onRefine }) {
  const [isEditing, setIsEditing] = useState(false)
  const [editedContent, setEditedContent] = useState(section.content)
  const [showRefine, setShowRefine] = useState(false)
  const [refineFeedback, setRefineFeedback] = useState('')
  const [refining, setRefining] = useState(false)
  const [originalContent, setOriginalContent] = useState(section.content)
  const [isComparing, setIsComparing] = useState(false)

  const handleSave = () => {
    onRefine(section.name, editedContent)
    setIsEditing(false)
  }

  const handleCancel = () => {
    setEditedContent(section.content)
    setIsEditing(false)
  }

  const handleRefine = async () => {
    if (!refineFeedback.trim()) return

    setRefining(true)
    try {
      const response = await axios.post(
        config.api.endpoints.refineSection,
        {
          section_name: section.name,
          current_content: section.content,
          user_feedback: refineFeedback
        }
      )

      setOriginalContent(section.content)
      setEditedContent(response.data.refined_content)
      setIsComparing(true)
      setShowRefine(false)
      setRefineFeedback('')
    } catch (error) {
      console.error('Error refining section:', error)
      alert('Failed to refine section. Please try again.')
    } finally {
      setRefining(false)
    }
  }

  const acceptRefined = () => {
    onRefine(section.name, editedContent)
    setIsComparing(false)
    setOriginalContent(editedContent)
  }

  const rejectRefined = () => {
    setEditedContent(originalContent)
    setIsComparing(false)
  }

  return (
    <div className="pdd-section">
      <div className="section-header">
        <h3>{section.name}</h3>
        <div className="section-actions">
          {!isComparing && !isEditing && (
            <>
              <button
                className="btn-icon"
                onClick={() => setIsEditing(true)}
                title="Edit section"
              >
                ✏️
              </button>
              <button
                className="btn-icon"
                onClick={() => setShowRefine(!showRefine)}
                title="AI Refine"
              >
                ✨
              </button>
            </>
          )}
        </div>
      </div>

      {isComparing ? (
        <div className="comparison-view">
          <div className="comparison-panel">
            <h4>Original</h4>
            <div className="comparison-content original">{originalContent}</div>
          </div>
          <div className="comparison-panel">
            <h4>Refined</h4>
            <div className="comparison-content refined">{editedContent}</div>
          </div>
          <div className="comparison-actions">
            <button className="btn btn-small btn-primary" onClick={acceptRefined}>
              Accept Refined
            </button>
            <button className="btn btn-small btn-secondary" onClick={rejectRefined}>
              Reject
            </button>
          </div>
        </div>
      ) : isEditing ? (
        <div className="edit-view">
          <textarea
            className="edit-textarea"
            value={editedContent}
            onChange={(e) => setEditedContent(e.target.value)}
            rows={10}
          />
          <div className="edit-actions">
            <button className="btn btn-small btn-primary" onClick={handleSave}>
              Save
            </button>
            <button className="btn btn-small btn-secondary" onClick={handleCancel}>
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div
          className="section-content"
          dangerouslySetInnerHTML={{
            __html: DOMPurify.sanitize(section.content)
          }}
        />
      )}

      {showRefine && !isEditing && !isComparing && (
        <div className="refine-panel">
          <textarea
            className="refine-textarea"
            placeholder="Describe how you'd like to improve this section..."
            value={refineFeedback}
            onChange={(e) => setRefineFeedback(e.target.value)}
            rows={3}
          />
          <div className="refine-actions">
            <button
              className="btn btn-small btn-primary"
              onClick={handleRefine}
              disabled={refining || !refineFeedback.trim()}
            >
              {refining ? 'Refining...' : '✨ AI Refine'}
            </button>
            <button
              className="btn btn-small btn-secondary"
              onClick={() => setShowRefine(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default PDDSection
