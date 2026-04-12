import requests
from django.core.cache import cache


def get_github_repos(username, max_repos=6):
    if not username:
        return []
    
    cache_key = f'github_repos_{username}'
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    try:
        url = f'https://api.github.com/users/{username}/repos'
        params = {
            'sort': 'updated',
            'per_page': max_repos
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            repos = response.json()
            repo_data = []
            
            for repo in repos[:max_repos]:
                if not repo.get('fork', False):
                    repo_data.append({
                        'name': repo.get('name', ''),
                        'description': repo.get('description', ''),
                        'language': repo.get('language', 'Unknown'),
                        'stars': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                        'url': repo.get('html_url', ''),
                        'updated': repo.get('updated_at', '')[:10],
                    })
            
            cache.set(cache_key, repo_data, 86400)  # 24 hours
            return repo_data
    except Exception:
        pass
    
    return []
