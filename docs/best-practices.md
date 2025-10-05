# Best Practices

## API Usage

1. **Always use environment variables** for API keys
2. **Implement error handling** for API calls
3. **Use streaming** for long responses
4. **Cache responses** when appropriate

## Code Organization

1. **Separate concerns**: Keep tools, agents, and utilities separate
2. **Reuse common code**: Use the `common/` module
3. **Document your code**: Add docstrings and comments
4. **Test your code**: Write tests for critical functionality

## Security

1. **Never commit `.env`** files
2. **Validate user inputs** before sending to API
3. **Sanitize tool outputs** before displaying
4. **Use rate limiting** in production

## Performance

1. **Use async/await** for concurrent requests
2. **Batch requests** when possible
3. **Stream responses** for better UX
4. **Monitor token usage** to control costs
