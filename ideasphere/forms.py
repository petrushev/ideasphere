from wtforms import Form, BooleanField, StringField, TextAreaField, SubmitField, \
    IntegerField, FileField

class AddMissionForm(Form):

    title = StringField('Title')
    description = TextAreaField('Description')
    submit = SubmitField('Add')

class AddProblemForm(Form):

    mission_id = IntegerField('mission_id')
    title = StringField('Title')
    description = TextAreaField('Description')
    submit = SubmitField('Add')

class ProposalForm(Form):

    problem_id = IntegerField('problem_id')
    title = StringField('Title')
    description = TextAreaField('Description')
    img = FileField('Image')
    model = FileField('Model')
    submit = SubmitField('Submit')
