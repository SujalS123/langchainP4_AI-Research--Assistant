/**
 * Utility functions for formatting text responses from LLM
 */

/**
 * Removes markdown formatting from text to display clean, plain text
 * @param {string} text - The text with markdown formatting
 * @returns {string} - Clean text without markdown formatting
 */
export function stripMarkdown(text) {
  if (!text || typeof text !== 'string') {
    return text;
  }

  return text
    // Remove bold formatting (**text**)
    .replace(/\*\*(.*?)\*\*/g, '$1')
    // Remove italic formatting (*text*)
    .replace(/\*(.*?)\*/g, '$1')
    // Remove headers (## Header, ### Header, etc.)
    .replace(/^#{1,6}\s+/gm, '')
    // Remove bullet points (* item, - item, + item)
    .replace(/^[\*\-\+]\s+/gm, '')
    // Remove numbered lists (1. item)
    .replace(/^\d+\.\s+/gm, '')
    // Remove inline code (`code`)
    .replace(/`(.*?)`/g, '$1')
    // Remove code blocks (```code```)
    .replace(/```[\s\S]*?```/g, (match) => {
      return match.replace(/```/g, '').trim();
    })
    // Remove links [text](url) -> keep just text
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    // Remove blockquotes (> quote)
    .replace(/^>\s+/gm, '')
    // Remove horizontal rules (---, ***)
    .replace(/^[\-\*]{3,}$/gm, '')
    // Clean up extra whitespace
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/**
 * Formats text for display by removing markdown and preserving readability
 * @param {string} text - The raw text from LLM
 * @returns {string} - Formatted clean text
 */
export function formatLLMResponse(text) {
  if (!text) return '';
  
  return stripMarkdown(text);
}
