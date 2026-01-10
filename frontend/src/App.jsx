import { useState } from 'react'
import React from 'react'
import axios from 'axios'
import PDDSection from './components/PDDSection'
import DiagramViewer from './components/DiagramViewer'
import './App.css'

function App() {
  const [processText, setProcessText] = useState('')
  const [uploadedFile, setUploadedFile] = useState(null)
  const [pddData, setPddData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const generatePDD = async () => {
    if (!processText.trim() && !uploadedFile) {
      setError('Please enter a process description or upload a file')
      return
    }

    setLoading(true)
    setError('')
    setPddData(null)

    try {
      if (uploadedFile) {
        // File upload takes priority, but we can also include text
        const formData = new FormData()
        formData.append('file', uploadedFile)

        const response = await axios.post('/api/upload-and-process-json', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        // If there's also text, we could append it or use it as context
        // For now, file processing is standalone
        setPddData(response.data)
      } else if (processText.trim()) {
        // Text-only input
        const response = await axios.post('/api/generate-pdd-json', {
          process_text: processText
        })
        setPddData(response.data)
      }
    } catch (err) {
      console.error('Error generating PDD:', err)
      if (err.response) {
        setError(`Server error: ${err.response.data.detail || 'Unknown error'}`)
      } else if (err.request) {
        setError('No response from server. Make sure the backend is running on http://localhost:8000')
      } else {
        setError(`Error: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  const clearForm = () => {
    setProcessText('')
    setUploadedFile(null)
    setPddData(null)
    setError('')
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const allowedTypes = ['.pdf', '.docx', '.mp4', '.mov', '.avi']
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase()

      if (!allowedTypes.includes(fileExtension)) {
        setError(`Unsupported file type: ${fileExtension}. Please use PDF, DOCX, MP4, MOV, or AVI.`)
        setUploadedFile(null)
        return
      }

      setUploadedFile(file)
      setError('')
    }
  }

  const handleRemoveFile = () => {
    setUploadedFile(null)
  }

  const handleSectionRefine = (sectionName, newContent) => {
    if (pddData) {
      const updatedSections = pddData.sections.map(section =>
        section.name === sectionName
          ? { ...section, content: newContent }
          : section
      )
      setPddData({ ...pddData, sections: updatedSections })
    }
  }

  const exportDocument = async (format) => {
    if (!pddData) return

    setLoading(true)
    try {
      if (format === 'pdf') {
        const response = await axios.post('/api/export-pdd', {
          process_name: pddData.process_name,
          sections: pddData.sections,
          diagram_code: pddData.diagram_code,
          format: format
        })

        const printWindow = window.open('', '_blank')
        printWindow.document.write(response.data)
        printWindow.document.close()
        setTimeout(() => {
          printWindow.print()
        }, 500)
      } else {
        const response = await axios.post('/api/export-pdd', {
          process_name: pddData.process_name,
          sections: pddData.sections,
          diagram_code: pddData.diagram_code,
          format: format
        }, {
          responseType: 'blob'
        })

        const blob = new Blob([response.data])
        const url = URL.createObjectURL(blob)
        const a = window.document.createElement('a')
        a.href = url

        const extensions = {
          'docx': 'docx',
          'html': 'html'
        }
        a.download = `PDD_${pddData.process_name.replace(/[^a-z0-9]/gi, '_')}.${extensions[format] || format}`
        a.click()
        URL.revokeObjectURL(url)
      }
    } catch (error) {
      console.error('Export error:', error)
      alert(`Failed to export as ${format.toUpperCase()}. Please try again.`)
    } finally {
      setLoading(false)
    }
  }

  const exportToPDF = () => exportDocument('pdf')
  const exportToWord = () => exportDocument('docx')
  const exportToHTML = () => exportDocument('html')

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>AI-Powered PDD Generator</h1>
          <p className="subtitle">Generate UiPath Process Design Documents with interactive editing</p>
        </header>

        <div className="input-section">
          <label htmlFor="process-text" className="label">
            Process Description (Optional)
          </label>
          <textarea
            id="process-text"
            className="textarea"
            placeholder="Enter your process description here...&#10;&#10;Example:&#10;The invoice processing process begins when an invoice is received via email. The finance clerk opens the email attachment and verifies the invoice amount against the purchase order. If the amount is correct and under $1000, they approve it for payment. If the amount is over $1000, manager approval is required. Once approved, the invoice is entered into the ERP system and marked for payment.&#10;&#10;You can also upload a document or video below."
            value={processText}
            onChange={(e) => setProcessText(e.target.value)}
            rows={8}
            disabled={loading}
          />

          <div className="divider">OR</div>

          <label htmlFor="file-upload" className="label">
            Upload Document or Video (Optional)
          </label>
          <div className="file-upload-area">
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.docx,.mp4,.mov,.avi"
              onChange={handleFileChange}
              disabled={loading}
            />
            {uploadedFile && (
              <div className="file-info">
                <strong>Selected file:</strong> {uploadedFile.name}
                <span className="file-size">({(uploadedFile.size / 1024 / 1024).toFixed(2)} MB)</span>
                <button
                  className="btn-remove-file"
                  onClick={handleRemoveFile}
                  disabled={loading}
                >
                  Remove
                </button>
              </div>
            )}
          </div>
          <p className="file-hint">
            Supported formats: PDF, DOCX, MP4, MOV, AVI
          </p>

          <div className="button-group">
            <button
              className="btn btn-primary"
              onClick={generatePDD}
              disabled={loading || (!processText.trim() && !uploadedFile)}
            >
              {loading ? 'Processing...' : 'Generate PDD'}
            </button>
            <button
              className="btn btn-secondary"
              onClick={clearForm}
              disabled={loading}
            >
              Clear
            </button>
          </div>

          {/* Export buttons - shown after PDD is generated */}
          {pddData && (
            <div className="export-section">
              <label className="label">Export Options</label>
              <div className="button-group">
                <button
                  className="btn btn-small btn-primary"
                  onClick={exportToPDF}
                  disabled={loading}
                >
                  Export PDF
                </button>
                <button
                  className="btn btn-small btn-primary"
                  onClick={exportToWord}
                  disabled={loading}
                >
                  Export Word
                </button>
                <button
                  className="btn btn-small"
                  onClick={exportToHTML}
                  disabled={loading}
                >
                  Export HTML
                </button>
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* PDD Output Section */}
        {pddData && (
          <div className="output-section">
            <div className="output-header">
              <h2>{pddData.process_name}</h2>
            </div>

            <div className="sections-container">
              {pddData.sections.map((section, index) => {
                // Find first matching section index for diagram placement
                const diagramSectionIndex = pddData.sections.findIndex(s =>
                  s.name === "Process Overview (AS IS)" ||
                  s.name === "High Level Process Map (AS IS)" ||
                  s.name === "Detailed Process Map (AS IS)"
                )
                const showDiagramAfter = diagramSectionIndex >= 0 && index === diagramSectionIndex

                return (
                  <React.Fragment key={index}>
                    <PDDSection
                      section={section}
                      onRefine={handleSectionRefine}
                    />
                    {showDiagramAfter && pddData.diagram_code && (
                      <DiagramViewer diagramCode={pddData.diagram_code} />
                    )}
                  </React.Fragment>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
