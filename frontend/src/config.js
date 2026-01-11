/**
 * Centralized application configuration.
 *
 * This file contains all configuration settings for the frontend application.
 * Environment variables can be used to override defaults for different environments.
 */

/**
 * API base URL configuration.
 *
 * In development, defaults to localhost:8000.
 * In production, should be set via VITE_API_URL environment variable.
 *
 * To set the API URL for different environments:
 * - Development: Create .env file with VITE_API_URL=http://localhost:8000
 * - Production: Set VITE_API_URL environment variable before build
 *
 * @type {string}
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * Application configuration object.
 *
 * Export all configuration settings here to maintain a single source of truth.
 */
const config = {
  api: {
    baseURL: API_BASE_URL,
    // API endpoints
    endpoints: {
      generatePDD: '/generate-pdd',
      generatePDDJson: '/api/generate-pdd-json',
      uploadAndProcess: '/upload-and-process',
      uploadAndProcessJson: '/api/upload-and-process-json',
      refineSection: '/refine-section',
      chat: '/chat',
      exportPDD: '/api/export-pdd',
      health: '/health'
    },
    // Timeout for API requests (in milliseconds)
    timeout: 120000 // 2 minutes
  },
  // Application settings
  app: {
    name: 'AI-Powered PDD Generator',
    version: '1.0.0'
  },
  // Feature flags
  features: {
    enableVideoUpload: true,
    enableRefinement: true,
    enableExport: true
  }
}

export default config
