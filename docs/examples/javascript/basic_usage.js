/**
 * LLM Hub JavaScript API Examples
 * Basic usage examples for interacting with LLM Hub services
 */

class LLMHubClient {
    /**
     * Initialize the client
     * @param {string} gatewayUrl - URL to the LLM Hub gateway
     * @param {string} apiKey - API key for authentication
     */
    constructor(gatewayUrl = 'http://localhost:8080', apiKey = 'changeme') {
        this.gatewayUrl = gatewayUrl.replace(/\/$/, '');
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }

    /**
     * Check the health status of the gateway
     * @returns {Promise<Object>} Health status object
     */
    async checkHealth() {
        const response = await fetch(`${this.gatewayUrl}/health`);
        if (!response.ok) {
            throw new Error(`Health check failed: ${response.status}`);
        }
        return response.json();
    }

    /**
     * Get list of available MCP tools
     * @returns {Promise<Array>} Array of tool objects
     */
    async listTools() {
        const response = await fetch(`${this.gatewayUrl}/mcp/tools`, {
            headers: this.headers
        });
        if (!response.ok) {
            throw new Error(`Failed to list tools: ${response.status}`);
        }
        const data = await response.json();
        return data.tools || [];
    }

    /**
     * Generate text using the inference tool
     * @param {string} prompt - Text prompt for generation
     * @param {string} model - Model name to use
     * @param {number} temperature - Sampling temperature (0.0 to 1.0)
     * @param {number} maxTokens - Maximum tokens to generate
     * @returns {Promise<string>} Generated text
     */
    async generateText(prompt, model, temperature = 0.7, maxTokens = 1000) {
        const payload = {
            parameters: {
                prompt,
                model,
                temperature,
                max_tokens: maxTokens
            }
        };

        const response = await fetch(`${this.gatewayUrl}/tools/inference`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Text generation failed: ${response.status}`);
        }

        const data = await response.json();
        return data.result || '';
    }

    /**
     * Get list of available models
     * @returns {Promise<Array>} Array of model objects
     */
    async listModels() {
        const payload = { parameters: {} };

        const response = await fetch(`${this.gatewayUrl}/tools/list_models`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Failed to list models: ${response.status}`);
        }

        const data = await response.json();
        return data.result?.models || [];
    }
}

/**
 * Main example function
 */
async function main() {
    console.log('LLM Hub JavaScript API Examples');
    console.log('='.repeat(40));

    const client = new LLMHubClient();

    try {
        // Check health
        console.log('\n1. Checking health status...');
        const health = await client.checkHealth();
        console.log(`   Status: ${health.status || 'unknown'}`);
        console.log(`   Version: ${health.version || 'unknown'}`);

        // List available tools
        console.log('\n2. Listing available tools...');
        const tools = await client.listTools();
        console.log(`   Found ${tools.length} tools:`);
        tools.forEach(tool => {
            console.log(`   - ${tool.name || 'unknown'}: ${tool.description || 'No description'}`);
        });

        // List available models
        console.log('\n3. Listing available models...');
        const models = await client.listModels();
        console.log(`   Found ${models.length} models:`);
        models.forEach(model => {
            console.log(`   - ${model.id || 'unknown'}: ${model.name || 'No name'}`);
        });

        // Generate text (if models are available)
        if (models.length > 0) {
            console.log('\n4. Generating text...');
            const modelId = models[0].id;
            const prompt = 'Write a short poem about artificial intelligence.';

            console.log(`   Using model: ${modelId}`);
            console.log(`   Prompt: ${prompt}`);

            const result = await client.generateText(
                prompt,
                modelId,
                0.8,
                200
            );

            console.log('   Generated text:');
            console.log(`   ${result}`);
        } else {
            console.log('\n4. No models available for text generation');
        }

    } catch (error) {
        console.error(`\nError: ${error.message}`);
    }
}

/**
 * Browser-specific implementation with DOM interaction
 */
if (typeof window !== 'undefined') {
    window.LLMHubClient = LLMHubClient;

    window.runExample = async function() {
        const outputEl = document.getElementById('output');
        if (outputEl) {
            outputEl.innerHTML = 'Running example...\n';
        }

        // Override console.log to display in browser
        const originalLog = console.log;
        console.log = function(...args) {
            originalLog.apply(console, args);
            if (outputEl) {
                outputEl.innerHTML += args.join(' ') + '\n';
            }
        };

        try {
            await main();
        } finally {
            console.log = originalLog;
        }
    };
}

// Node.js specific
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        LLMHubClient,
        main
    };

    // Auto-run if called directly
    if (require.main === module) {
        main().catch(console.error);
    }
}
