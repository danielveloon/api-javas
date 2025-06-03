Primeiro você roda ``pip install -r .\requirements.txt`` e depois ``./run.bat``

ai só testar esse curl

``curl --location 'http://127.0.0.1:5000/predict_covid' \
--header 'Content-Type: application/json' \
--data '{
    "Problema Respiratório": "Não",
    "Febre": "Sim",
    "Tosse Seca": "Sim",
    "Dor de Garganta": "Não",
    "Coriza": "Sim",
    "Asma": "Não",
    "Doença Pulmonar Crônica": "Não",
    "Dor de Cabeça": "Sim",
    "Doença Cardíaca": "Não",
    "Diabetes": "Não",
    "Hipertensão": "Sim",
    "Fadiga": "Sim",
    "Problemas Gastrointestinais": "Não",
    "Viagem ao Exterior": "Não",
    "Contato com Paciente COVID": "Sim",
    "Participou de Multidão": "Sim",
    "Visitou Locais Públicos": "Sim",
    "Familiar em Local Público": "Não"
  }'``