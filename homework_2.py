import requests
import hashlib
import json

class PeopleClientEroor(Exception):
    pass

class PeopleClient:

    RESPONSE_DICT = ('first_name', 'last_name', 'email', 'phone', 'ip_address')

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def get_all(self, limit=None):
        if limit is None:
            return requests.get(self.base_url).json()
        if limit <= 0:
            raise ValueError('Limit has to be positive.')

        response = requests.get(self.base_url, params={'_limit': limit})
        total_records = int(response.headers['X-Total-Count'])
        pages_count= total_records // limit

        if total_records % limit != 0:
            pages_count += 1
        people = response.json()

        for page in range(2, pages_count + 1):
            chunk=requests.get(self.base_url, params={'_limit': limit, '_page': page}).json()

            people.extend(chunk)
            #for person in chunk:
            #    people.append(person)
        return people

    def add_person(self, first_name, last_name, email, phone, ip_adress):
        headers = {'Authorization': 'Bearer ' + self.token}
        person = {'first_name': first_name,
                  'last_name': last_name,
                  'email': email,
                  'phone': phone,
                  'ip_address': ip_adress}
        response = requests.post(self.base_url, json=person, headers=headers)
        if response.status_code != 201: #if not respons.ok
            raise PeopleClientEroor(response.json()['error'])
        return response.json()

    def person_by_id(self, person_id):
        url = self.base_url + person_id
        response = requests.get(url)
        #response.raise_for_status()
        if response.status_code == 404:
            raise PeopleClientEroor('User with given id not found')
        elif not response.ok:
            raise PeopleClientEroor('Unknown error.')
        return response.json()

    def query(self, **criteria):
        for key in criteria:
            if key not in self.RESPONSE_DICT:
                raise ValueError('Unknown error' + key)
        return requests.get(self.base_url, params={**criteria})

    def people_by_partial_ip(self, partial_ip):
        ip_regexp = '^' + partial_ip
        return requests.get(self.base_url, params={'ip_addres_like': ip_regexp}).json()

    def delete_by_id(self,id):
        person_id=self.base_url + id
        response=requests.delete(person_id)

        if response.status_code==404:
            raise PeopleClientEroor('User with given id not found and not delete')
        elif not response.ok:
            raise PeopleClientEroor('Unknown error.')
        return 'Data delete'

    def delete_by_name(self, name):
        response=requests.get(self.base_url, params={'first_name': name}).json()
        count_delete=0
        for value in response:
            person_id = self.base_url + str(value['id'])
            response=requests.delete(person_id)
            if response.status_code==200:
                count_delete +=1
        return count_delete


    def add_from_file(self, my_file):
        headers = {'Authorization': 'Bearer ' + self.token}
        with open(my_file, 'rt') as json_file:
            file=json.load(json_file)
        for item in file:
            response = requests.post(self.base_url, json=item, headers=headers)
            if response.status_code !=201:
                raise PeopleClientEroor('error')
            return 'Data saved'

        return json.dumps(responses)


if __name__ == '__main__':
    token = hashlib.md5('relayr'.encode('ascii')).hexdigest()
    client = PeopleClient('http://polakow.eu:3000/people/', token)


#people=client.get_all()

#people2 = client.person_by_id('fRHs_u8')
#print(people2)

#print(client.add_person('Gosia', 'Jamroży', 'gosia.jamrozy@nteria.pl', '+48632039104', '192.191.1.2'))

#print("Deleted records : ", client.delete_by_name('Gosia'))

#print(people == people2)

#people3 = client.person_by_id('CfJJMuh')
#print(people3)


#janusze = client.query(first_name='Janusz', last_name='Polak', ip_address='0.0.0.0').json()
#print(janusze)

#search_ip=client.people_by_partial_ip('192.168')
#print(search_ip)


print(client.add_from_file('test_data.json'))

print(client.delete_by_id('19910215'))

print("Deleted records : ", client.delete_by_name('Gosia'))
