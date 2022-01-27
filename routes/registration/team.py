from flask import request
from routes.registration.validation import TeamRegistrationValidation
from marshmallow import ValidationError
from models.team import TeamModel
from flask_restful import Resource
from models.contestant import ContestantModel
from models.registration import RegistrationModel
from constants import MAXIMUM_RESERVISTS, CONTESTANT_COUNTS

class TeamRegistration(Resource):
    def post(self):
        data = request.get_json()
        schema = TeamRegistrationValidation()

        try:
            schema.load(data)
        except ValidationError as err:
            return {"messages": err.messages}, 400

        #0    
        existing_team = TeamModel.find_id_by_name(data['name'])
        if existing_team:
            return "EXISTING_TEAM", 400

        for contestant in data['contestants']:
            if not 'role' in contestant:
                return "U jednoho z účastníků chybí role", 400
            if not 'externist' in contestant:
                return "U jednoho z účastníků chybí informace o tom, jestli je z jiné školy", 400

        if data['game'] == "ROCKET_LEAGUE":
            for contestant in data['contestants']:
                if not 'epicId' in contestant:
                    return "U jednoho z účastníků chybí epic ID", 400

        if data['game'] == "COUNTER_STRIKE":
            for contestant in data['contestants']:
                if not 'csRank' in contestant:
                    return "U jednoho z účastníků chybí rank", 400
                if not 'maxCsRank' in contestant:
                    return "U jednoho z účastníků chybí maximální rank", 400
                if not 'faceitLevel' in contestant:
                    return "U jednoho z účastníků chybí faceit level", 400
                if not 'maxFaceitLevel' in contestant:
                    return "U jednoho z účastníků chybí maximální faceit level", 400

        captain_count = 0
        reservist_count = 0
        externist_count = 0
        for contestant in data['contestants']:
            if contestant['role'] == 'CAPTAIN':
                captain_count += 1
            if contestant['role'] == 'RESERVIST':
                reservist_count += 1
            if contestant['externist']:
                externist_count += 1
        if externist_count > 1:
            return "Maximální počet účasntíků z jiné školy je 1", 400
        if reservist_count > MAXIMUM_RESERVISTS:
            return "Maximální počet záložníků je 2"
        if captain_count == 0:
            return "Tým musí mít alespoň jednoho kapitána", 400
        if captain_count > 1:
            return "Tým nesmí mít více než jednoho kapitána", 400
        if len(data['contestants']) == 1 and externist_count == 1:
            return "Tým nesmí obsahovat pouze externistu"
        contestant_counts = CONTESTANT_COUNTS[data['game']]
        contestant_count = len(data['contestants']) - reservist_count
        if contestant_count > contestant_counts['max']:
            return "Byl přesažen maximální počet účastníků", 400
        if contestant_count < contestant_counts['min']:
            return "Není dosažen minimální počet účastníků", 400
        
        contestant_id_list = []
        registered_contestant_list = []
        unregistered_contestant_list = []        
        for contestant in data['contestants']:
            id = ContestantModel.find_id_by_email(contestant['email'])
            if id:
                contestant_id_list.append(id)
                registered_contestant_list.append(contestant)
            else:
                contestant_id_list.append(contestant['email'])
                unregistered_contestant_list.append(contestant)

        #Remove duplicate ids
        contestant_id_list_2 = list(set(contestant_id_list))

        #1
        if len(contestant_id_list) != len(contestant_id_list_2):
            return "SAME_EMAIL", 400

        #2
        for id in contestant_id_list:
            if RegistrationModel.exists(id, data['game']):
                return "CONTESTANT_ALREADY_REGISTERED", 400

        for contestant_config in unregistered_contestant_list:
            if not contestant_config['externist']:
                contestant_config['schoolId'] = data['schoolId']
            else:
                contestant_config['schoolId'] = None
            contestant = ContestantModel(contestant_config)
            contestant.insert()
        team = TeamModel(data['name'], data['game'], data['schoolId'])
        team.insert()

        team_id = TeamModel.find_id_by_name(data['name'])
        for contestant_config in data['contestants']:
            contestant_id = ContestantModel.find_id_by_email(contestant_config['email'])
            contestant = ContestantModel.find_by_id(contestant_id)
            contestant.update(contestant_config)
            registration = RegistrationModel({
                'teamId': team_id,
                'game': data['game'],
                'nickname': contestant_config['nickname'],
                'contestantId': contestant_id,
                'externist': contestant_config['externist'],
                'role': contestant_config['role']
            })
            registration.insert()
            
        return "", 200

        

       
        
        
