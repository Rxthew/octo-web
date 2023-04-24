import re
import requests
from requests.auth import HTTPBasicAuth


#Original Octosuite class lifted from repository pared down to relevant properties.
class Octosuite:
    def __init__(self):
        # API endpoint
        self.endpoint = 'https://api.github.com'

        # Path attribute
        self.path_attrs = ['size', 'type', 'path', 'sha', 'html_url']
        # Path attribute dictionary
        self.path_attr_dict = {'size': 'Size (bytes)',
                               'type': 'Type',
                               'path': 'Path',
                               'sha': 'SHA',
                               'html_url': 'URL'}

        # organisation attributes
        self.org_attrs = ['avatar_url', 'login', 'id', 'node_id', 'email', 'description', 'blog', 'location',
                          'followers',
                          'following', 'twitter_username', 'public_gists', 'public_repos', 'type', 'is_verified',
                          'has_organisation_projects', 'has_repository_projects', 'created_at', 'updated_at']
        # organisation attribute dictionary
        self.org_attr_dict = {'avatar_url': 'Profile Photo',
                              'login': 'Username',
                              'id': 'ID',
                              'node_id': 'Node ID',
                              'email': 'Email',
                              'description': 'About',
                              'location': 'Location',
                              'blog': 'Blog',
                              'followers': 'Followers',
                              'following': 'Following',
                              'twitter_username': 'Twitter handle',
                              'public_gists': 'Gists',
                              'public_repos': 'Repositories',
                              'type': 'Account type',
                              'is_verified': 'Is verified?',
                              'has_organisation_projects': 'Has organisation projects?',
                              'has_repository_projects': 'Has repository projects?',
                              'created_at': 'Created at',
                              'updated_at': 'Updated at'}

        # Repository attributes
        self.repo_attrs = ['id', 'description', 'forks', 'stargazers_count', 'watchers', 'license', 'default_branch',
                           'visibility',
                           'language', 'open_issues', 'topics', 'homepage', 'clone_url', 'ssh_url', 'fork',
                           'allow_forking',
                           'private', 'archived', 'has_downloads', 'has_issues', 'has_pages', 'has_projects',
                           'has_wiki',
                           'pushed_at', 'created_at', 'updated_at']
        # Repository attribute dictionary
        self.repo_attr_dict = {'id': 'ID',
                               'description': 'About',
                               'forks': 'Forks',
                               'stargazers_count': 'Stars',
                               'watchers': 'Watchers',
                               'license': 'License',
                               'default_branch': 'Branch',
                               'visibility': 'Visibility',
                               'language': 'Language(s)',
                               'open_issues': 'Open issues',
                               'topics': 'Topics',
                               'homepage': 'Homepage',
                               'clone_url': 'Clone URL',
                               'ssh_url': 'SSH URL',
                               'fork': 'Is fork?',
                               'allow_forking': 'Is forkable?',
                               'private': 'Is private?',
                               'archived': 'Is archived?',
                               'is_template': 'Is template?',
                               'has_wiki': 'Has wiki?',
                               'has_pages': 'Has pages?',
                               'has_projects': 'Has projects?',
                               'has_issues': 'Has issues?',
                               'has_downloads': 'Has downloads?',
                               'pushed_at': 'Pushed at',
                               'created_at': 'Created at',
                               'updated_at': 'Updated at'}

        # Repo releases attributes
        self.repo_releases_attrs = ['id', 'node_id', 'tag_name', 'target_commitish', 'assets', 'draft', 'prerelease',
                                    'created_at',
                                    'published_at']
        # Repo releases attribute dictionary
        self.repo_releases_attr_dict = {'id': 'ID',
                                        'node_id': 'Node ID',
                                        'tag_name': 'Tag',
                                        'target_commitish': 'Branch',
                                        'assets': 'Assets',
                                        'draft': 'Is draft?',
                                        'prerelease': 'Is prerelease?',
                                        'created_at': 'Created at',
                                        'published_at': 'Published at'}

        # Profile attributes
        self.profile_attrs = ['avatar_url', 'login', 'id', 'node_id', 'bio', 'blog', 'location', 'followers',
                              'following',
                              'twitter_username', 'public_gists', 'public_repos', 'company', 'hireable', 'site_admin',
                              'created_at',
                              'updated_at']
        # Profile attribute dictionary
        self.profile_attr_dict = {'avatar_url': 'Profile Photo',
                                  'login': 'Username',
                                  'id': 'ID',
                                  'node_id': 'Node ID',
                                  'bio': 'Bio',
                                  'blog': 'Blog',
                                  'location': 'Location',
                                  'followers': 'Followers',
                                  'following': 'Following',
                                  'twitter_username': 'Twitter Handle',
                                  'public_gists': 'Gists (public)',
                                  'public_repos': 'Repositories (public)',
                                  'company': 'organisation',
                                  'hireable': 'Is hireable?',
                                  'site_admin': 'Is site admin?',
                                  'created_at': 'Joined at',
                                  'updated_at': 'Updated at'}

        # User attributes
        self.user_attrs = ['avatar_url', 'id', 'node_id', 'gravatar_id', 'site_admin', 'type', 'html_url']
        # User attribute dictionary
        self.user_attr_dict = {'avatar_url': 'Profile Photo',
                               'id': 'ID',
                               'node_id': 'Node ID',
                               'gravatar_id': 'Gravatar ID',
                               'site_admin': 'Is site admin?',
                               'type': 'Account type',
                               'html_url': 'URL'}

        # Topic attributes
        self.topic_attrs = ['score', 'curated', 'featured', 'display_name', 'created_by', 'created_at', 'updated_at']
        # Topic attribute dictionary
        self.topic_attr_dict = {'score': 'Score',
                                'curated': 'Curated',
                                'featured': 'Featured',
                                'display_name': 'Display name',
                                'created_by': 'Created by',
                                'created_at': 'Created at',
                                'updated_at': 'Updated at'}

        # Gists attribute
        self.gists_attrs = ['node_id', 'description', 'comments', 'files', 'git_push_url', 'public', 'truncated',
                            'updated_at']
        # Gists attribute dictionary
        self.gists_attr_dict = {'node_id': 'Node ID',
                                'description': 'About',
                                'comments': 'Comments',
                                'files': 'Files',
                                'git_push_url': 'Git Push URL',
                                'public': 'Is public?',
                                'truncated': 'Is truncated?',
                                'updated_at': 'Updated at'}

        # Issue attributes
        self.issue_attrs = ['id', 'node_id', 'score', 'state', 'number', 'comments', 'milestone', 'assignee',
                            'assignees', 'labels',
                            'locked', 'draft', 'closed_at']
        # Issue attribute dict
        self.issue_attr_dict = {'id': 'ID',
                                'node_id': 'Node ID',
                                'score': 'Score',
                                'state': 'State',
                                'closed_at': 'Closed at',
                                'number': 'Number',
                                'comments': 'Comments',
                                'milestone': 'Milestone',
                                'assignee': 'Assignee',
                                'assignees': 'Assignees',
                                'labels': 'Labels',
                                'draft': 'Is draft?',
                                'locked': 'Is locked?',
                                'created_at': 'Created at'}

        # Repo issues attributes
        self.repo_issues_attrs = ['id', 'node_id', 'state', 'reactions', 'number', 'comments', 'milestone', 'assignee',
                                  'active_lock_reason', 'author_association', 'assignees', 'labels', 'locked',
                                  'closed_at',
                                  'created_at', 'updated_at']
        # Issue attribute dict
        self.repo_issues_attr_dict = {'id': 'ID',
                                      'node_id': 'Node ID',
                                      'number': 'Number',
                                      'state': 'State',
                                      'reactions': 'Reactions',
                                      'comments': 'Comments',
                                      'milestone': 'Milestone',
                                      'assignee': 'Assignee',
                                      'assignees': 'Assignees',
                                      'author_association': 'Author association',
                                      'labels': 'Labels',
                                      'locked': 'Is locked?',
                                      'active_lock_reason': 'Lock reason',
                                      'closed_at': 'Closed at',
                                      'created_at': 'Created at',
                                      'updated_at': 'Updated at'}

        # User organisations attributes
        self.user_orgs_attrs = ['avatar_url', 'id', 'node_id', 'url', 'description']
        self.user_orgs_attr_dict = {'avatar_url': 'Profile Photo',
                                    'id': 'ID',
                                    'node_id': 'Node ID',
                                    'url': 'URL',
                                    'description': 'About'}

        # Author dictionary
        self.author_dict = {'Alias': 'rly0nheart',
                            'Country': ':zambia: Zambia, Africa',
                            'About.me': 'https://about.me/rly0nheart',
                            'Buy Me A Coffee': 'https://buymeacoffee.com/189381184'}

    def get_repos_from_username(self, username):
        response = requests.get(f"{self.endpoint}/users/{username}/repos?per_page=100&sort=pushed",
                                auth=HTTPBasicAuth(username, '')).text
        repositories = re.findall(rf'"full_name":"{username}/(.*?)",.*?"fork":(.*?),', response)
        unforked_repos = []
        for repository in repositories:
            if repository[1] == 'false':
                unforked_repos.append(repository[0])
        return unforked_repos

    def get_email_from_contributor(username, repo, contributor):
        response = requests.get(f"https://github.com/{username}/{repo}/commits?author={contributor}",
                                auth=HTTPBasicAuth(username, '')).text
        latest_commit = re.search(rf'href="/{username}/{repo}/commit/(.*?)"', response)
        if latest_commit:
            latest_commit = latest_commit.group(1)
        else:
            latest_commit = 'dummy'
        commit_details = requests.get(f"https://github.com/{username}/{repo}/commit/{latest_commit}.patch",
                                    auth=HTTPBasicAuth(username, '')).text
        email = re.search(r'<(.*)>', commit_details)
        if email:
            email = email.group(1)
        return email




#Inherit octosuite class and make applicable changes.
def new_octosuite_class():

    def response_resolver(link, request_details):
        details = request_details
        url_patterns = {
            'organisation': f"{details['endpoint']}/orgs/{details['reference']}/{details['resource']}?per_page={details['limit']}",
            'repository': f"{details['endpoint']}/repos/{details['reference']}/{details['repo_name']}/{details['resource']}?per_page={details['limit']}",
            'search': f"{details['endpoint']}/{details['reference']}?={details['query']}&per_page={details['limit']}",
            'user': f"{details['endpoint']}/users/{details['reference']}/{details['resource']}?per_page={details['limit']}",
        }
        url_to_use = url_patterns[details['pattern']]
        return requests.get(link) if link else  requests.get(url_to_use)


    """
    data_handler is a helper which abstracts repetitive logic. It
    returns an object which runs a given function and returns some
    data based on the status header coming from a given response.

    Examples of 'structure_to_organise' and 'subject_data' can include
    gists, repositories, organisations - and all their attributes.
    Each have a different key attributes such as id, login or name
    which is used as a reference to access other attributes.

    See user profile as an example of similar - though not analogous -
    implementation.    
    
    """

    def data_handler(structure_to_organise, error_msg, json_response, index=None):
        def organise_data():
            empty_subject_data = [sub for sub in json_response[f'{index}']] if index else [sub for sub in json_response] 
            
            def add_attributes(sub):
                subject_key = sub[f'{structure_to_organise["key"]}']
                subject_attrs = structure_to_organise['attrs']
                attr_dict = structure_to_organise['attr_dict']
                new_subject_data = {f'{subject_key}': {}}
                for attr in subject_attrs:
                    new_subject_data[f'{subject_key}'].update({f'{attr_dict[attr]}' : sub[attr]})
                return new_subject_data

            subject_data = map(add_attributes,empty_subject_data)
            return subject_data

        def not_found():
            return {'error': f'{error_msg}'}
        
        def default_response():
                print(json_response) #remove
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}

        return {
            200: organise_data,
            404: not_found,
            'default': default_response
        }

    def process_final_response(body,links):
        return {'body': list(body), 'links': links} if type(body) is map else body

    class Octo_Web(Octosuite):
        def __init__(self):
            super().__init__()

        def about(self):
            about_text = f"""
            OCTOSUITE © 2023 Richard Mwewa
                    
            An advanced and lightning fast framework for gathering open-source intelligence on GitHub users and organizations.
            Read the wiki: https://github.com/bellingcat/octosuite/wiki
            GitHub REST API documentation: https://docs.github.com/rest
            """
            return about_text

        def author(self):
            author = {
                'name': 'Richard Mwewa (Ritchie)',
            }
            for author_key, author_value in self.author_dict.items():
                author.update({f'{author_key}' : f'{author_value}'})
            
            return author

        def commits_search(self, query, limit=10):
            response = requests.get(f"{self.endpoint}/search/commits?q={query}/&per_page={limit}")
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'No commits were found.'}

            def commit_not_found():
                return {'error': 'No commits were found.'}

            def default_response():
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}
            
            def commit_data():
                raw_commit_data = [commit for commit in json_response['items']]

                def populate_commit_data(commit):
                    commit_data = {
                        commit['commit']['tree']['sha'] : {}
                    }
                    commit_search_tree = commit_data[f"{commit['commit']['tree']['sha']}"]
                    commit_search_tree.update({
                        'Author': f"{commit['commit']['author']['name']}",
                        'Username': f"{commit['author']['login']}",
                        'Email': f"{commit['commit']['author']['email']}",
                        'Commiter': f"{commit['commit']['committer']['name']}",
                        'Repository': f"{commit['repository']['full_name']}",
                        'URL': f"{commit['html_url']}",
                        'message': f"{commit['commit']['message']}"

                    })

                commits_data = map(populate_commit_data,raw_commit_data)
                return commits_data 
                  
            handle_response = {
                404: commit_not_found,
                200: commit_data,
                'default': default_response

            }

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def get_user_email(self, username):
            repos = self.get_repos_from_username(username)
            for repo in repos:
                email = self.get_email_from_contributor(username, repo, username)
                if email:
                    return {'f{username}': email }
            return {'error': 'User e-mail not found.'}

        def issues_search(self, query, limit=10):
            request_details = {
                'endpoint': self.endpoint,
                'reference': 'issues',
                'query': query,
                'limit': limit,
                'pattern': 'search',
                'repo_name': False,
                
            } 

            response = response_resolver(request_details)
            json_response = response.json()

            if(json_response == 'error'):
                return {'error' : 'No issues were found found for that query.'}

            issue_data = {
                'key': 'title',
                'attrs': self.repo_issues_attrs,
                'attr_dict': self.repo_issues_attr_dict
            }

            handle_response = data_handler(issue_data, 'No issues were found found for that query.', json_response, 'items')

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            
            return handle_response[status_code]()

        def org_events(self, organisation, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'events',
                'reference': organisation,
                'limit': limit,
                'pattern': 'organisation',
                'repo_name': False,
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            def org_event_not_found():
                return {'error': 'Organisation not found.'}

            def default_response():
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}
            
            def org_event_data():
                raw_events_data = [event for event in json_response]

                def populate_event_data(event):
                    event.update({
                        'Type': f"{event['type']}",
                        'Created at': f"{event['created_at']}",
                        'Payload': f"{event['payload']}"
                    })

                events_data = map(populate_event_data,raw_events_data)
                return events_data 
                  
            handle_response = {
                404: org_event_not_found,
                200: org_event_data,
                'default': default_response

            }

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()
        
        def org_member(self, organisation, username):

            response = requests.get(f"{self.endpoint}/orgs/{organisation}/public_members/{username}")
            
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'Organisation or user was not found.'}

            member = response.status_code and response.status_code == 204
            
            return  f'POSITIVE: User {username} is a public member of {organisation}' if member else f'NEGATIVE: User {username} is not a public member of {organisation}' 

        def org_profile(self, organisation):

            response = requests.get(f"{self.endpoint}/orgs/{organisation}")

            def organisation_profile_not_found():
                return {'error': 'Organisation not found.'}

            def default_response():
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}
            
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'Organisation not found.'}
            
            def organisation_profile_data():
                profile = {
                    'name': json_response['name'],
                }
                for attr in self.org_attrs:
                    profile.update({f'{self.org_attr_dict[attr]}' : json_response[attr]})
                
                return profile 
                  
            handle_response = {
                404: organisation_profile_not_found,
                200: organisation_profile_data,
                'default': default_response

            }

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()


        def org_repos(self, organisation, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'repos',
                'reference': organisation,
                'limit': limit,
                'pattern': 'organisation',
                'repo_name': False,
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'Organisation does not have repositories.'}
            
            repos_data = {
                'key': 'full_name',
                'attrs': self.repo_attrs,
                'attr_dict': self.repo_attr_dict
            }

            handle_response = data_handler(repos_data, 'Organisation not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()
        
        def path_contents(self, username, repo_name,path_name):
            
            response = requests.get(f"{self.endpoint}/repos/{username}/{repo_name}/contents/{path_name}")

            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'Path content not found.'}

            def path_content_data():
                raw_content = [{content_count : content} for content_count, content in enumerate(json_response,start=1)]

                def add_path_attributes(content):
                    raw_value = content.items()[0]
                    count = content.keys()[0]
                    path_contents = {
                        'name': raw_value['name'],
                        'count': count                  
                    }     
                    for attr in self.path_attrs:
                        path_contents.update({
                            f"{self.path_attr_dict[attr]}": raw_value[attr]
                        })
                    return path_contents

                new_content = map(add_path_attributes,raw_content)
                return new_content
                  
            def path_not_found():
                return {'error': 'Path contents not found.'}

            def default_response():
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}
            
            
            handle_response = {
                    404: path_not_found,
                    200: path_content_data,
                    'default': default_response
            }

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def repo_contributors(self, username, repo_name, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'contributors',
                'reference': username,
                'repo_name': repo_name,
                'limit': limit,
                'pattern': 'repository',
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'Repository does not have contributors.'}
            
            repos_data = {
                'key': 'login',
                'attrs': self.user_attrs,
                'attr_dict': self.user_attr_dict
            }

            handle_response = data_handler(repos_data, 'Repository or user not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def repo_forks(self, username, repo_name,limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'forks',
                'reference': username,
                'repo_name': repo_name,
                'limit': limit,
                'pattern': 'repository',
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'Repository does not have forks.'}

            repos_data = {
                'key': 'full_name',
                'attrs': self.repo_attrs,
                'attr_dict': self.repo_attr_dict
            }

            handle_response = data_handler(repos_data, 'Repository or user not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def repo_issues(self, username, repo_name, limit=10):

            issues_attrs = self.repo_issues_attrs.copy()
            issues_attrs.append('body')

            issues_attr_dict = self.repo_issues_attr_dict.copy()
            issues_attr_dict['body'] = 'Body'

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'issues',
                'reference': username,
                'repo_name': repo_name,
                'limit': limit,
                'pattern': 'repository',
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'Repository does not have open issues.'}
            
            repos_data = {
                'key': 'name',
                'attrs': issues_attrs,
                'attr_dict': issues_attr_dict
            }

            handle_response = data_handler(repos_data, 'Repository or user not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()  

        def repo_releases(self, username, repo_name, limit=10):

            releases_attrs = self.repo_releases_attrs.copy()
            releases_attrs.append('body')

            releases_attr_dict = self.repo_releases_attr_dict.copy()
            releases_attr_dict['body'] = 'Body'

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'releases',
                'reference': username,
                'repo_name': repo_name,
                'limit': limit,
                'pattern': 'repository',
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'Repository does not have releases.'}
            
            repos_data = {
                'key': 'name',
                'attrs': releases_attrs,
                'attr_dict': releases_attr_dict
            }

            handle_response = data_handler(repos_data, 'Repository or user not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()  

        def repo_stargazers(self, username, repo_name, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'stargazers',
                'reference': username,
                'repo_name': repo_name,
                'limit': limit,
                'pattern': 'repository',
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'Repository does not have stargazers.'}
            
            repos_data = {
                'key': 'login',
                'attrs': self.user_attrs,
                'attr_dict': self.user_attr_dict
            }

            handle_response = data_handler(repos_data, 'Repository or user not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()              

        def repos_search(self, query, limit=10):
            request_details = {
                'endpoint': self.endpoint,
                'reference': 'repositories',
                'query': query,
                'limit': limit,
                'pattern': 'search',
                'repo_name': False,
                                
            } 

            response = response_resolver(request_details)
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'No repositories were found found for that query.'}

            repo_data = {
                'key': 'full_name',
                'attrs': self.repo_attrs,
                'attr_dict': self.repo_attr_dict
            }

            handle_response = data_handler(repo_data, 'No repositories were found found for that query.', json_response, 'items')

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            
            return handle_response[status_code]()

        def topics_search(self, query, limit=10):
            request_details = {
                'endpoint': self.endpoint,
                'reference': 'topics',
                'query': query,
                'limit': limit,
                'pattern': 'search',
                'repo_name': False               
            } 

            response = response_resolver(request_details)
            json_response = response.json()

            if(json_response == 'error'):
                return {'error' : 'No topics were found found for that query.'}

            topic_data = {
                'key': 'name',
                'attrs': self.topic_attrs,
                'attr_dict': self.topic_attr_dict
            }

            handle_response = data_handler(topic_data, 'No topics were found found for that query.', json_response, 'items')

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            
            return handle_response[status_code]()

        def user_events(self, username, limit=10):

            response = requests.get(f"{self.endpoint}/users/{username}/events/public?per_page={limit}")
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'User is not involved in any events.'}

            def user_event_not_found():
                return {'error': 'User not found.'}

            def default_response():
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}
            
            def user_event_data():
                raw_events_data = [event for event in json_response]

                def populate_event_data(event):
                    event_data = {
                        event['id'] : {}
                    }
                    event_data[f'{event["id"]}'].update({
                        'Actor': f"{event['actor']['login']}",
                        'Type': f"{event['type']}",
                        'Repository': f"{event['repo']['name']}",
                        'Created at': f"{event['created_at']}",
                        'Payload': f"{event['payload']}"

                    })

                events_data = map(populate_event_data,raw_events_data)
                return events_data 
                  
            handle_response = {
                404: user_event_not_found,
                200: user_event_data,
                'default': default_response

            }

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def user_followers(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'followers',
                'reference': username,
                'limit': limit,
                'pattern': 'user',
                'repo_name': False,
                'query': False                
            } 

            response = response_resolver(request_details)
            json_response = response.json()

            if(json_response == 'error'):
                return {'error' : 'User does not have any followers.'}

            user_data = {
                'key': 'login',
                'attrs': self.user_attrs,
                'attr_dict': self.user_attr_dict
            }

            handle_response = data_handler(user_data, 'User not found.', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            
            return handle_response[status_code]()
        
        def user_following(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'following',
                'reference': username,
                'limit': limit,
                'pattern': 'user',
                'repo_name': False,
                'query': False
            } 

            response = response_resolver(request_details)
            json_response = response.json()

            if(json_response == 'error'):
                return {'error' : 'User is not following any other user.'}

            user_data = {
                'key': 'login',
                'attrs': self.user_attrs,
                'attr_dict': self.user_attr_dict
            }

            handle_response = data_handler(user_data, 'User not found.', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()
        
        def user_follows(self, following_username, followed_username):

            response = requests.get(f"{self.endpoint}/users/{following_username}/following/{followed_username}")
            
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'One or more users were not found.'}

            following = response.status_code and response.status_code == 204
            
            return  f'POSITIVE: {following_username} is following {followed_username}' if following else f'NEGATIVE: {following_username} is not following {following_username}' 

        def user_gists(self, username,limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'gists',
                'reference': username,
                'limit': limit,
                'pattern': 'user',
                'repo_name': False,
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'User does not have gists'}
            
            gist_data = {
                'key': 'id',
                'attrs': self.gists_attrs,
                'attr_dict': self.gists_attr_dict
            }

            handle_response = data_handler(gist_data, 'User not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def user_orgs(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'orgs',
                'reference': username,
                'limit': limit,
                'pattern': 'user',
                'repo_name': False,
                'query': False
            }

            response = response_resolver(request_details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'User neither belongs to nor owns any organisations'}
            
            orgs_data = {
                'key': 'login',
                'attrs': self.org_attrs,
                'attr_dict': self.org_attr_dict
            }

            handle_response = data_handler(orgs_data, 'User not found', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def user_profile(self, username):
            response = requests.get(f"{self.endpoint}/users/{username}")

            def user_profile_not_found():
                return {'error': 'User not found.'}

            def default_response():
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}
            
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'User not found'}
            
            def user_profile_data():
                profile = {
                    'name': json_response['name'],
                }
                for attr in self.profile_attrs:
                    profile.update({f'{self.profile_attr_dict[attr]}' : json_response[attr]})
                
                return profile 
                  
            handle_response = {
                404: user_profile_not_found,
                200: user_profile_data,
                'default': default_response

            }

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()

        def user_repos(self, username, limit=10, page_link=None):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'repos',
                'reference': username,
                'limit': limit,
                'pattern': 'user',
                'repo_name': False,
                'query': False
            } 

            response = response_resolver(page_link,request_details)
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'User does not have repositories.'}

            repo_data = {
                'key': 'full_name',
                'attrs': self.repo_attrs,
                'attr_dict': self.repo_attr_dict
            }

            handle_response = data_handler(repo_data, 'User not found.', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            body = handle_response[status_code]()
            links = response.links
            return process_final_response(body,links)

        def user_search(self, query, limit=10):
            request_details = {
                'endpoint': self.endpoint,
                'reference': 'users',
                'query': query,
                'limit': limit,
                'pattern': 'search',
                'repo_name': False,
            } 

            response = response_resolver(request_details)
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'No users were found found for that query.'}

            user_data = {
                'key': 'login',
                'attrs': self.user_attrs,
                'attr_dict': self.user_attr_dict
            }

            handle_response = data_handler(user_data, 'No users were found found for that query.', json_response, 'items')

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            
            return handle_response[status_code]()

        def user_subscriptions(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'subscriptions',
                'reference': username,
                'limit': limit,
                'pattern': 'user',
                'repo_name': False,
                'query': False
            } 

            response = response_resolver(request_details)
            json_response = response.json()

            if(json_response == 'error'):
                return {'error' : 'User does not have any subscriptions.'}

            subscription_data = {
                'key': 'full_name',
                'attrs': self.repo_attrs,
                'attr_dict': self.repo_attr_dict
            }

            handle_response = data_handler(subscription_data, 'User not found.', json_response)

            status_code = response.status_code if response.status_code == 404 or response.status_code == 200 else 'default'
            return handle_response[status_code]()


    return Octo_Web



            

        
            

    
