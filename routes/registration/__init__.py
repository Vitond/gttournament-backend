from routes.registration.alone import AloneRegistration
from routes.registration.team import TeamRegistration

registrationRoutes = [
    (AloneRegistration, '/alone'),
    (TeamRegistration, '/team')
]