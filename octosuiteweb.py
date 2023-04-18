import requests
from octosuite import octosuite;

#Inherit original octosuite class and make applicable changes.
def new_octosuite_class():

    def response_resolver(details):
        def unlimited_response():
            return requests.get(f"{details.endpoint}/users/{details.username}/{details.resource}")

        def limited_response():
            return requests.get(f"{details.endpoint}/users/{details.username}/{details.resource}?per_page={details.limit}") 

        response = limited_response() if details.limit else unlimited_response()
        return response


    def data_handler(structure_to_organise, error_msg, json_response):
        def organise_data():
            empty_subject_data = [sub for sub in json_response]
            
            def add_attributes(sub):
                subject_key = sub[f'{structure_to_organise.key}']
                subject_attrs = structure_to_organise.attrs
                attr_dict = structure_to_organise['attr_dict']
                new_subject_data = {f'{subject_key}': {}}
                for attr in subject_attrs:
                    new_subject_data[f'{subject_key}'].update({f'{attr_dict[attr]}' : sub[attr]})
                return new_subject_data

            subject_data = map(add_attributes,empty_subject_data)
            return subject_data

        def not_found():
            return {'error': f'{error_msg}'}

        return {
            200: organise_data,
            404: not_found,
            'default': json_response
        }


    Octo_Source = octosuite.Octosuite
    class Octo_Web(Octo_Source):
        def __init__(self):
            super().__init__(self)

        #Override applicable methods to fetch information
        def user_profile(self, username):
            response = requests.get(f"{self.endpoint}/users/{username}")

            def user_profile_not_found():
                return {'error': 'User not found.'}
            
            json_response = response.json()  
            
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
                'default': json_response

            }

            status_code = response.status_code or 'default'
            return handle_response[status_code]()
        
        def get_user_email(self, username):
            repos = self.get_repos_from_username(username)
            for repo in repos:
                email = self.get_email_from_contributor(username, repo, username)
                if email:
                    return {'f{username}': email }
            return {'error': 'User e-mail not found.'}

        def user_repos(self, username, limit):

            details = {
                'endpoint': self.endpoint,
                'resource': 'repos',
                'username': username,
                'limit': limit
            } 

            response = response_resolver(details)
            json_response = response.json()

            repo_data = {
                'key': 'full_name',
                'attrs': self.repo_attrs,
                'attr_dict': self.repo_attr_dict
            }

            handle_response = data_handler(repo_data, 'User not found.', json_response)

            status_code = response.status_code or 'default'
            return handle_response[status_code]()
        
        def user_gists(self, username,limit):

            details = {
                'endpoint': self.endpoint,
                'resource': 'gists',
                'username': username,
                'limit': limit
            }

            response = response_resolver(details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'User does not have gists'}
            
            gist_data = {
                'key': 'id',
                'attrs': self.gists_attrs,
                'attr_dict': self.gists_attr_dict
            }

            handle_response = data_handler(gist_data, 'User not found', json_response)

            status_code = response.status_code or 'default'
            return handle_response[status_code]()

        def user_orgs(self, username, limit):

            details = {
                'endpoint': self.endpoint,
                'resource': 'orgs',
                'username': username,
                'limit': limit
            }

            response = response_resolver(details)
            json_response = response.json() or 'error'
            
            if(json_response == 'error'):
                return {'error' : 'User neither belongs to nor owns any organisations'}
            
            orgs_data = {
                'key': 'login',
                'attrs': self.org_attrs,
                'attr_dict': self.org_attr_dict
            }

            handle_response = data_handler(orgs_data, 'User not found', json_response)

            status_code = response.status_code or 'default'
            return handle_response[status_code]()


    return Octo_Web



            

        
            

    
