/**
 * Application configuration loaded from environment variables
 */

// App metadata
export const APP_NAME = 'Alfabroker Admin';
export const APP_VERSION = '0.0.1';

// API configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';
export const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 30000;

// Environment
export const IS_DEV = import.meta.env.DEV;
export const IS_PROD = import.meta.env.PROD;
