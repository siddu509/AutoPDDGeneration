import { useState } from 'react'
import axios from 'axios'
import PDDSection from './components/PDDSection'
import DiagramViewer from './components/DiagramViewer'
import ChatWidget from './components/ChatWidget'
import './App.css'

function App() {
  const [processText, setProcessText] = useState('')
  const [uploadedFile, setUploadedFile] = useState(null)
  const [generatedPDD, setGeneratedPDD] = useState(null) // For HTML mode
  const [pddData, setPddData] = useState(null) // For interactive mode
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [inputMode, setInputMode] = useState('text') // 'text' or 'file'
  const [viewMode, setViewMode] = useState('html') // 'html' or 'interactive'

  const generatePDD = async (useJsonApi = false) => {
    if (inputMode === 'text' && !processText.trim()) {
      setError('Please enter a process description')
      return
    }

    if (inputMode === 'file' && !uploadedFile) {
      setError('Please upload a file')
      return
    }

    setLoading(true)
    setError('')
    setGeneratedPDD(null)
    setPddData(null)

    try {
      if (inputMode === 'text') {
        if (useJsonApi) {
          // Use JSON API for interactive mode
          const response = await axios.post('/api/generate-pdd-json', {
            process_text: processText
          })
          setPddData(response.data)
        } else {
          // Use HTML API for classic mode
          const response = await axios.post('/generate-pdd', {
            process_text: processText
          }, {
            headers: { 'Content-Type': 'application/json' }
          })
          setGeneratedPDD(response.data)
        }
      } else {
        // File upload
        const formData = new FormData()
        formData.append('file', uploadedFile)

        const endpoint = useJsonApi ? '/api/upload-and-process-json' : '/upload-and-process'
        const response = await axios.post(endpoint, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        if (useJsonApi) {
          setPddData(response.data)
        } else {
          setGeneratedPDD(response.data)
        }
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
    setGeneratedPDD(null)
    setPddData(null)
    setError('')
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const allowedTypes = ['.pdf', '.docx', '.mp4', '.mov', '.avi']
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase()

      if (!allowedTypes.includes(fileExtension)) {
        setError(`Unsupported file type: ${fileExtension}. Please use PDF, DOCX, or MP4.`)
        setUploadedFile(null)
        return
      }

      setUploadedFile(file)
      setError('')
    }
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
        // For PDF, open in new window and trigger print
        const response = await axios.post('/api/export-pdd', {
          process_name: pddData.process_name,
          sections: pddData.sections,
          diagram_code: pddData.diagram_code,
          format: format
        })

        // Open in new window and print
        const printWindow = window.open('', '_blank')
        printWindow.document.write(response.data)
        printWindow.document.close()
        setTimeout(() => {
          printWindow.print()
        }, 500)
      } else {
        // For Word and HTML, download the file
        const response = await axios.post('/api/export-pdd', {
          process_name: pddData.process_name,
          sections: pddData.sections,
          diagram_code: pddData.diagram_code,
          format: format
        }, {
          responseType: 'blob'
        })

        // Create blob and download
        const blob = new Blob([response.data])
        const url = URL.createObjectURL(blob)
        const a = window.document.createElement('a')
        a.href = url

        // Set file extension based on format
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
          {/* View Mode Toggle */}
          <div className="mode-toggle">
            <button
              className={`mode-btn ${viewMode === 'html' ? 'active' : ''}`}
              onClick={() => setViewMode('html')}
            >
              Classic View
            </button>
            <button
              className={`mode-btn ${viewMode === 'interactive' ? 'active' : ''}`}
              onClick={() => setViewMode('interactive')}
            >
              Interactive View
            </button>
          </div>

          {/* Input Mode Toggle */}
          <div className="mode-toggle">
            <button
              className={`mode-btn ${inputMode === 'text' ? 'active' : ''}`}
              onClick={() => setInputMode('text')}
            >
              Text Input
            </button>
            <button
              className={`mode-btn ${inputMode === 'file' ? 'active' : ''}`}
              onClick={() => setInputMode('file')}
            >
              File Upload
            </button>
          </div>

          {inputMode === 'text' ? (
            <>
              <label htmlFor="process-text" className="label">
                Process Description
              </label>
              <textarea
                id="process-text"
                className="textarea"
                placeholder="Enter your process description here...&#10;&#10;Example:&#10;The invoice processing process begins when an invoice is received via email. The finance clerk opens the email attachment and verifies the invoice amount against the purchase order. If the amount is correct and under $1000, they approve it for payment. If the amount is over $1000, manager approval is required. Once approved, the invoice is entered into the ERP system and marked for payment."
                value={processText}
                onChange={(e) => setProcessText(e.target.value)}
                rows={12}
              />
            </>
          ) : (
            <>
              <label htmlFor="file-upload" className="label">
                Upload Document or Video
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
                  </div>
                )}
              </div>
              <p className="file-hint">
                Supported formats: PDF, DOCX, MP4, MOV, AVI
              </p>
            </>
          )}

          <div className="button-group">
            <button
              className="btn btn-primary"
              onClick={() => generatePDD(viewMode === 'interactive')}
              disabled={loading}
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
        </div>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Interactive Mode */}
        {viewMode === 'interactive' && pddData && (
          <div className="output-section">
            <div className="output-header">
              <h2>{pddData.process_name}</h2>
              <div className="export-buttons">
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

            <DiagramViewer diagramCode={pddData.diagram_code} />

            <div className="sections-container">
              {pddData.sections.map((section, index) => (
                <PDDSection
                  key={index}
                  section={section}
                  onRefine={handleSectionRefine}
                />
              ))}
            </div>
          </div>
        )}

        {/* Classic HTML Mode */}
        {viewMode === 'html' && generatedPDD && (
          <div className="output-section">
            <div className="output-header">
              <h2>Generated PDD</h2>
              <button
                className="btn btn-small"
                onClick={() => {
                  const printWindow = window.open('', '_blank')
                  printWindow.document.write(generatedPDD)
                  printWindow.document.close()
                  printWindow.print()
                }}
              >
                Print / Save as PDF
              </button>
            </div>
            <div
              className="pdd-content"
              dangerouslySetInnerHTML={{ __html: generatedPDD }}
            />
          </div>
        )}
      </div>

      {/* Chat Widget - only show in interactive mode */}
      {viewMode === 'interactive' && (
        <ChatWidget context={processText} />
      )}
    </div>
  )
}

export default App
