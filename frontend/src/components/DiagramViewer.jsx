import { useEffect, useRef } from 'react'
import mermaid from 'mermaid'
import './DiagramViewer.css'

function DiagramViewer({ diagramCode }) {
  const containerRef = useRef(null)

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'default',
      flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
      },
      securityLevel: 'loose'
    })
  }, [])

  useEffect(() => {
    if (containerRef.current && diagramCode) {
      // Clear previous content
      containerRef.current.innerHTML = ''

      // Generate unique ID for this diagram
      const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`

      // Render the diagram
      mermaid.render(id, diagramCode).then((result) => {
        if (containerRef.current) {
          containerRef.current.innerHTML = result.svg
        }
      }).catch((error) => {
        console.error('Mermaid rendering error:', error)
        if (containerRef.current) {
          containerRef.current.innerHTML = `<p class="error">Failed to render diagram</p>`
        }
      })
    }
  }, [diagramCode])

  if (!diagramCode) {
    return null
  }

  return (
    <div className="diagram-viewer">
      <h3>Process Flow Diagram</h3>
      <div ref={containerRef} className="diagram-container" />
    </div>
  )
}

export default DiagramViewer
