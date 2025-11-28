/**
 * Application configuration constants.
 * These values are loaded from environment variables at build time.
 */

/**
 * Base URL for the API.
 * In development: http://localhost:8000/api/v1
 * In production: Set via VITE_API_BASE_URL environment variable
 */
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
