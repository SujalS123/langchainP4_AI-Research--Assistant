/**
 * Test file to demonstrate the markdown formatting functionality
 */
import { stripMarkdown, formatLLMResponse } from './textFormatter.js';

// Test the formatter with the example text from the user
const testText = `✨
Research Summary
Okay, based on the search results, here's a summary of where you can find the latest tech news:

**Key Sources for Latest Tech News:**

*   **Reuters:** Provides technology news from around the globe.
*   **PCMag:** Offers in-depth analysis and news from expert analysts.
*   **WIRED:** Covers technology, science, culture, and business.
*   **Google News (Technology):** A broad overview of advancements, trends, and news in technology.
*   **AP News:** Provides up-to-date tech news.
*   **TechCrunch:** Focuses on the business of technology, startups, venture capital, and Silicon Valley.
*   **Gadgets 360:** Delivers technology news, gadget reviews, mobile updates, and more, with a focus on India and the world.
*   **TechSpot:** Highlights trending stories in technology.
*   **The Verge:** Covers hardware, apps, and tech from major companies to startups.`;

console.log('=== ORIGINAL TEXT ===');
console.log(testText);
console.log('\n=== FORMATTED TEXT ===');
console.log(formatLLMResponse(testText));

// Test individual markdown patterns
console.log('\n=== INDIVIDUAL TESTS ===');
console.log('Bold test:', stripMarkdown('**This is bold** text'));
console.log('Italic test:', stripMarkdown('*This is italic* text'));
console.log('Header test:', stripMarkdown('## This is a header'));
console.log('Bullet test:', stripMarkdown('* This is a bullet point'));
console.log('Number test:', stripMarkdown('1. This is numbered'));
console.log('Code test:', stripMarkdown('This has `inline code` here'));
console.log('Link test:', stripMarkdown('This has a [link](http://example.com) here'));
