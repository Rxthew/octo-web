import requests
from octosuite import octosuite;

#Inherit original octosuite class and make applicable changes.
def new_octosuite_class():

    def response_resolver(request_details):
        details = request_details
        url_patterns = {
            'user': f"{details['endpoint']}/users/{details['username']}/{details['resource']}?per_page={details['limit']}",
            'search': f"{details['endpoint']}/{details['group']}?={details['query']}&per_page={details['limit']}",
            'organisation': f"{details['endpoint']}/orgs/{details['organisation']}/{details['resource']}?per_page={details['limit']}",

        }
        url_to_use = url_patterns[details['pattern']]
        return requests.get(url_to_use)


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
                return {'error': 'Something unexpected happened. Please check your internet connection and try again.'}

        return {
            200: organise_data,
            404: not_found,
            'default': default_response
        }


    Octo_Source = octosuite.Octosuite
    class Octo_Web(Octo_Source):
        def __init__(self):
            super().__init__()

        #Override applicable methods to fetch information

        def org_events(self, organisation, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'events',
                'organisation': organisation,
                'limit': limit,
                'pattern': 'organisation'
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
                'organisation': organisation,
                'limit': limit,
                'pattern': 'organisation'
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
        
        def get_user_email(self, username):
            repos = self.get_repos_from_username(username)
            for repo in repos:
                email = self.get_email_from_contributor(username, repo, username)
                if email:
                    return {'f{username}': email }
            return {'error': 'User e-mail not found.'}

        def user_repos(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'repos',
                'username': username,
                'limit': limit,
                'pattern': 'user'
            } 

            response = response_resolver(request_details)
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
            return handle_response[status_code]()
        
        def user_gists(self, username,limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'gists',
                'username': username,
                'limit': limit,
                'pattern': 'user'
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
                'username': username,
                'limit': limit,
                'pattern': 'user'
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

        def user_subscriptions(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'subscriptions',
                'username': username,
                'limit': limit,
                'pattern': 'user'
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
        
        def user_following(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'following',
                'username': username,
                'limit': limit,
                'pattern': 'user'
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

        def user_followers(self, username, limit=10):

            request_details = {
                'endpoint': self.endpoint,
                'resource': 'followers',
                'username': username,
                'limit': limit,
                'pattern': 'user'
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
        
        def user_follows(self, following_username, followed_username):

            response = requests.get(f"{self.endpoint}/users/{following_username}/following/{followed_username}")
            
            json_response = response.json() or 'error'

            if(json_response == 'error'):
                return {'error' : 'One or more users were not found.'}

            following = response.status_code and response.status_code == 204
            
            return  f'POSITIVE: {following_username} is following {followed_username}' if following else f'NEGATIVE: {following_username} is not following {following_username}' 

        def user_search(self, query, limit=10):
            request_details = {
                'endpoint': self.endpoint,
                'group': 'users',
                'query': query,
                'limit': limit,
                'pattern': 'search'
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

        def repos_search(self, query, limit=10):
            request_details = {
                'endpoint': self.endpoint,
                'group': 'repositories',
                'query': query,
                'limit': limit,
                'pattern': 'search'
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
                'group': 'topics',
                'query': query,
                'limit': limit,
                'pattern': 'search'
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

        def issues_search(self, query, limit=10):
            request_details = {
                'endpoint': self.endpoint,
                'group': 'issues',
                'query': query,
                'limit': limit,
                'pattern': 'search'
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

    return Octo_Web



            

        
            

    
