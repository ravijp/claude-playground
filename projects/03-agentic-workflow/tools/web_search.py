def search_web(query):
    """Simulated web search"""
    # In production, integrate with real search API
    results = {
        "python version": "Python 3.13 is the latest stable version released in 2024",
        "claude ai": "Claude is an AI assistant created by Anthropic, launched in 2023",
        "latest": "Current year is 2025"
    }
    
    query_lower = query.lower()
    for key, value in results.items():
        if key in query_lower:
            return value
    
    return f"Search results for '{query}': [Simulated results - integrate real API in production]"
