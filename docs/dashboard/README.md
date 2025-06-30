# LLM Hub Health Dashboard

A simple, self-contained HTML dashboard for monitoring the health and status of LLM Hub services.

## Features

- **Real-time Health Monitoring** - Check status of Gateway and Bridge services
- **Service Metrics** - View uptime, version, and service counts
- **Available Tools** - See all MCP tools currently available
- **Auto-refresh** - Automatically updates every 30 seconds
- **Responsive Design** - Works on desktop and mobile devices
- **No Dependencies** - Pure HTML/CSS/JavaScript, no external libraries

## Usage

### Quick Start

1. **Start LLM Hub services**
   ```bash
   cd ops/compose
   docker-compose up -d
   ```

2. **Open the dashboard**
   - Open `docs/dashboard/index.html` in your web browser
   - Or serve it via a web server for better CORS handling

3. **Configure endpoints** (if needed)
   - Gateway URL: Default `http://localhost:8080`
   - Bridge URL: Default `http://localhost:3000`
   - API Key: Default `changeme`

### Serving via Web Server

For better CORS handling and to avoid browser restrictions:

```bash
# Using Python
cd docs/dashboard
python -m http.server 8000

# Using Node.js (if you have npx)
cd docs/dashboard
npx serve .

# Using any other web server
# Then access: http://localhost:8000
```

## Dashboard Components

### Gateway Status Card
- **Status Indicator** - Green (healthy), Red (unhealthy), Gray (unknown)
- **Version** - Current gateway version
- **Uptime** - How long the gateway has been running
- **Services** - Number of healthy services out of total

### Bridge Status Card
- **Status Indicator** - Service health status
- **LM Studio** - Connection status to LM Studio
- **Service** - Bridge service status

### Available Tools Card
- **Tool Count** - Total number of available MCP tools
- **Tool Grid** - List of all tools with their service source
- **Status Indicator** - Whether tools are accessible

## Configuration

### Environment URLs

Update the URLs in the configuration section if your services run on different ports:

- **Gateway URL** - Where the unified gateway is accessible
- **Bridge URL** - Where the LM Studio bridge is accessible  
- **API Key** - Authentication key for accessing protected endpoints

### Custom Styling

The dashboard uses CSS custom properties that can be easily modified:

```css
:root {
  --primary-color: #3b82f6;
  --success-color: #10b981;
  --error-color: #ef4444;
  --warning-color: #f59e0b;
}
```

## Troubleshooting

### CORS Issues

If you see CORS errors in the browser console:

1. **Serve the dashboard via HTTP server** (recommended)
2. **Disable CORS in browser** (development only)
3. **Configure CORS in LLM Hub services** (if needed)

### Connection Issues

If services show as unhealthy:

1. **Check service URLs** - Ensure Gateway and Bridge URLs are correct
2. **Verify services are running** - Use `docker-compose ps` to check
3. **Check API key** - Ensure the API key matches your configuration
4. **Check network connectivity** - Try accessing URLs directly in browser

### Authentication Issues

If you get 401/403 errors:

1. **Check API key** - Ensure it matches the `API_KEY` in your `.env` file
2. **Verify authentication is enabled** - Check `AUTH_ENABLED` setting
3. **Try without authentication** - Set `AUTH_ENABLED=false` for testing

## Features in Detail

### Auto-refresh
- Automatically refreshes every 30 seconds
- Pauses when browser tab is hidden (saves resources)
- Manual refresh button available

### Status Indicators
- **Green (Healthy)** - Service is responding and healthy
- **Red (Unhealthy)** - Service is not responding or reporting errors
- **Gray (Unknown)** - Status check in progress or not yet performed

### Error Handling
- Shows detailed error messages when services are unreachable
- Graceful degradation when some services are unavailable
- Retry logic with manual refresh option

## Customization

### Adding New Metrics

To add new health metrics, modify the JavaScript:

```javascript
// Add new metric to a card
const newMetric = document.createElement('div');
newMetric.className = 'metric';
newMetric.innerHTML = `
    <span class="metric-label">New Metric</span>
    <span class="metric-value">Value</span>
`;
document.getElementById('gateway-metrics').appendChild(newMetric);
```

### Custom Themes

Modify the CSS variables in the `<style>` section to change colors and styling:

```css
/* Dark theme example */
body {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}

.card {
    background: #374151;
    color: white;
}
```

## Security Considerations

- **API Key Exposure** - The API key is visible in the browser. Use read-only keys if possible.
- **Local Access Only** - This dashboard is designed for local development/monitoring
- **HTTPS in Production** - Use HTTPS when deploying to production environments

## Browser Compatibility

- **Modern Browsers** - Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- **Mobile Browsers** - iOS Safari 12+, Chrome Mobile 60+
- **Features Used** - CSS Grid, Fetch API, ES6 features

## Development

To modify the dashboard:

1. **Edit HTML/CSS/JS** directly in `index.html`
2. **Test locally** by opening in browser or serving via HTTP
3. **Check browser console** for any JavaScript errors
4. **Test with different service states** (healthy, unhealthy, offline)

## Integration

The dashboard can be integrated into other monitoring systems:

- **Embed in iframe** - Include in other web applications
- **Extract metrics** - Use the JavaScript functions programmatically
- **Custom endpoints** - Modify to work with different health check APIs
