from marshmallow import Schema, fields, validate
from constants import GAMES, CS_RANKS, FACEIT_LEVELS, ROLES


class ContestantValidation(Schema):
    name = fields.Str(required=True, validate=[
        validate.Length(
            min=2,
            error='Jméno musí mít alespoň dva znaky'
        ),
        validate.Length(
            max=100,
            error='Jméno musí mít méně než 100 znaků'
        )
    ])
    nickname = fields.Str(required=True, validate=[
        validate.Length(
            min=2,
            error='Přezdívka musí mít alespoň dva znaky'
        ),
        validate.Length(
            max=100,
            error='Přezdívka musí mít méně než 100 znaků'
        )
    ])
    surname = fields.Str(required=True, validate=[
        validate.Length(
            min=2,
            error='Příjmení musí mít alespoň dva znaky'
        ),
        validate.Length(
            max=100,
            error='Příjmení musí mít méně než 100 znaků'
        )
    ])
    email = fields.Str(required=True, validate=[
        validate.Email(
            error='Zadaný email je neplatný'
        ),
        validate.Length(
            max=100,
            error='Email musí mít méně než 100 znaků'
        )
    ])
    adult = fields.Boolean(required=True)
    discord = fields.Str(required=True, validate = [
        validate.Regexp(
            regex = r'^(.+)#[0-9]{4}$',
            error = 'Zadaný discord je neplatný'
        )
    ])
    csRank = fields.Str(
        validate = [
            validate.OneOf(CS_RANKS)
        ]
    )
    maxCsRank = fields.Str(
        validate = [
            validate.OneOf(CS_RANKS)
        ]
    )
    faceitLevel = fields.Str(
        validate = [
            validate.OneOf(FACEIT_LEVELS)
        ]
    )
    externist = fields.Boolean()
    maxFaceitLevel = fields.Str(
        validate = [
            validate.OneOf(FACEIT_LEVELS)
        ]
    )
    epicId = fields.Str(
        validate = [
            validate.Length(
            min=2,
            error='Epic ID musí mít alespoň dva znaky'
            ),
            validate.Length(
                max=100,
                error='Epic ID musí mít méně než 100 znaků'
            )
        ]
    )
    role = fields.Str(
        calidate = [
            validate.OneOf(ROLES)
        ]
    )
    schoolId = fields.Integer(
        validate = [
            validate.Range(
                min=1
            )    
        ]
    )


class AloneRegistrationValidation(Schema):
    schoolId = fields.Integer(required=True,
        validate = [
            validate.Range(
                min=1
            )    
        ]
    )
    game = fields.Str(required=True, validate=[
        validate.OneOf(GAMES)
    ])
    contestant = fields.Nested(ContestantValidation, required=True)

class TeamRegistrationValidation(Schema):
    schoolId = fields.Integer(required=True,
        validate = [
            validate.Range(
                min=1
            )    
        ]
    )
    game = fields.Str(required=True, validate=[
        validate.OneOf(GAMES)
    ])
    name = fields.Str(required=True, validate=[
            validate.Length(
                min=2,
                error='Jméno týmu musí mít alespoň dva znaky'
                ),
            validate.Length(
                max=100,
                error='Jméno týmu musí mít méně než 100 znaků'
            )
    ])
    contestants = fields.List(fields.Nested(ContestantValidation), required=True)
    
