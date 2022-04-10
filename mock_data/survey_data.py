#pylint: skip-file

#region classes
class MockExercise():
    def __init__(self, survey_title, survey_type, questions, comments=None, construct_name=None, visibility="T"):
        self.survey_title = survey_title
        self.survey_type = survey_type
        self.construct_name = construct_name
        self.questions = questions
        self.comments = comments
        self.visibility = visibility

class MockQuestion():
    def __init__(self, question_type, body, required=True, construct_names=None):
      self.question_type = question_type
      self.body = body
      self.required = required
      self.construct_names = construct_names

class MockComment():
    def __init__(self, body, location):
        self.body = body
        self.location = location

class MockModel():
    def __init__(self, name, method, constructs):
        self.name = name
        self.method = method
        self.constructs = constructs

class MockConstruct():
    def __init__(self, name, construct_type, properties, children=None):
        self.name = name
        self.type = construct_type
        self.properties = properties
        self.children = children
#endregion classes

#region constructs
positive_trait_name = "positive_trait"
negative_trait_name = "negative_trait"
thermos_construct_types = [positive_trait_name, negative_trait_name]

anxiety_name = "Anxiety"
failure_avoidance_name = "Failure avoidance"
uncertain_control_name = "Uncertain control"
self_sabotage_name = "Self-sabotage"
disengagement_name = "Disengagement"
self_belief_name = "Self belief"
learning_focus_name = "Learning focus"
valuing_name = "Valuing"
persistence_name = "Persistence"
planning_name = "Planning"
task_management_name = "Task management"
interpersonal_group_work_skills_name = "Interpersonal group work skills"
task_group_work_skills_name = "Task group work skills"

thermos_models_and_constructs = [
    MockModel(name="MES", method="thermos_model", constructs=[
        MockConstruct(name="Negative Motivation", construct_type=negative_trait_name, properties={}, children=[
            MockConstruct(
                name=anxiety_name,
                construct_type=negative_trait_name,
                properties={
                    "norms": [51, 87],
                    "href": "https://thermos.sites.uu.nl/negative-motivation-uncertain-control-failure-avoidance-and-anxiety/#custom-collapse-0-2",
                    "feedback": "thermos.anxiety.feedback",
                    "importance": "thermos.anxiety.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Participating in the <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/persoonlijke-problemen-aanpakken/training-pak-stress-aan'>‘Pak stress aan’</a> training could help cope with feelings of anxiety or stress.</li>
                        <li>If you are experiencing problems due to anxiety, participating in a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen/persoonlijke-problemen-aanpakken/mindfulness-aandachttraining'>Mindfulness training</a> can be helpful (in Dutch, requires an intake interview).</li>
                        <li>Participating in a <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/tentamenworkshop'>‘Tentamenworkshop’</a> can reduce feelings of anxiety when an exam is coming up.</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Deelnemen aan de  <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/persoonlijke-problemen-aanpakken/training-pak-stress-aan'>‘Pak stress aan’</a> training kan helpen omgaan met gevoelens van stress of Anxiety.</li>
                        <li>Als je problemen ervaart door je Anxiety, kan het deelnemen aan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen/persoonlijke-problemen-aanpakken/mindfulness-aandachttraining'>Mindfulness training</a> helpen (in het Nederlands, een intake is vereist vooraf).</li>
                        <li>Deelnemen aan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/tentamenworkshop'>‘Tentamenworkshop’</a> kan helpen bij het verminderen van Anxiety wanneer er een tentamen aan komt.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        </ul>
                    "}
                    """
                }
            ),
            MockConstruct(
                name=failure_avoidance_name,
                construct_type=negative_trait_name,
                properties={
                    "norms": [24, 64],
                    "href": "https://thermos.sites.uu.nl/negative-motivation-uncertain-control-failure-avoidance-and-anxiety/#custom-collapse-0-1",
                    "feedback": "thermos.failure_avoidance.feedback",
                    "importance": "thermos.failure_avoidance.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        </ul>
                    "}
                    """
                }
            ),
            MockConstruct(
                name=uncertain_control_name,
                construct_type=negative_trait_name,
                properties={
                    "norms": [33, 69],
                    "href": "https://thermos.sites.uu.nl/negative-motivation-uncertain-control-failure-avoidance-and-anxiety/#custom-collapse-0-0",
                    "feedback": "thermos.uncertain_control.feedback",
                    "importance": "thermos.uncertain_control.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        <li>Following the course <a target='_blank' href='https://students.uu.nl/agenda/training-bewust-effectief-werken-nederlandstalig'>‘Bewust en effectief werken’</a> could also add to this aspect’s development.</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        <li>Het volgen van de cursus <a target='_blank' href='https://students.uu.nl/agenda/training-bewust-effectief-werken-nederlandstalig'>‘Bewust en effectief werken’</a> kan ook helpen bij het ontwikkelen van dit aspect.</li>
                        </ul>
                    "}
                    """
                }
            )
        ]),
        MockConstruct(name="Negative Engagement", construct_type=negative_trait_name, properties={}, children=[
            MockConstruct(
                name=self_sabotage_name,
                construct_type=negative_trait_name,
                properties={
                    "norms": [23, 63],
                    "href": "https://thermos.sites.uu.nl/negative-engagement-disengagement-and-self-sabotage/#custom-collapse-0-1",
                    "feedback": "thermos.self_sabotage.feedback",
                    "importance": "thermos.self_sabotage.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        <li>If you want help to further develop your planning skills, you can follow the course <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-timemanagement-en-studeren'>‘Time management en studeren’</a> (in Dutch).</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        <li>Als je graag hulp wil bij het beter leren plannen van je studie kan de workshop <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-timemanagement-en-studeren'>‘Time management en studeren’</a> helpen.</li>
                        </ul>
                    "}
                    """
                }
            ),
            MockConstruct(
                name=disengagement_name,
                construct_type=negative_trait_name,
                properties={
                    "norms": [25, 55],
                    "href": "https://thermos.sites.uu.nl/negative-engagement-disengagement-and-self-sabotage/#custom-collapse-0-0",
                    "feedback": "thermos.disengagement.feedback",
                    "importance": "thermos.disengagement.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        </ul>
                    "}
                    """
                }
            )
        ]),
        MockConstruct(name="Positive Motivation", construct_type=positive_trait_name, properties={}, children=[
            MockConstruct(
                name=self_belief_name,
                construct_type=positive_trait_name,
                properties={
                    "norms": [69, 93],
                    "href": "https://thermos.sites.uu.nl/positive-motivationself-belief-learning-focus-and-valuing/#custom-collapse-0-0",
                    "feedback": "thermos.self_belief.feedback",
                    "importance": "thermos.self_belief.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        <li>If you are experiencing issues with hindering self-belief, the course <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen/persoonlijke-problemen-aanpakken/verander-je-negatieve-zelfbeeld'>'Verander je negatieve zelfbeeld'</a> (Dutch only) can be helpful. (Take note: an intake interview is required before you can participate).</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        <li>Als je moeilijkheden ervaart door je mate van self-belief, kan de cursus <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen/persoonlijke-problemen-aanpakken/verander-je-negatieve-zelfbeeld'>'Verander je negatieve zelfbeeld'</a> helpen. (Voor deze cursus is een intake proces).</li>
                        </ul>
                    "}
                    """
                }
            ),
            MockConstruct(
                name=learning_focus_name,
                construct_type=positive_trait_name,
                properties={
                    "norms": [78, 94],
                    "href": "https://thermos.sites.uu.nl/positive-motivationself-belief-learning-focus-and-valuing/#custom-collapse-0-1",
                    "feedback": "thermos.learning_focus.feedback",
                    "importance": "thermos.learning_focus.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        <li>If you want help to further develop your learning focus and other academic skills, you can follow the course <a target='_blank' href='http://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-academisch-leren'>‘Smart study techniques’</a> or <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-academisch-leren'>‘Slim Studeren’</a>.</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        <li>Als je graag hulp wil bij het verder ontwikkelen van je learning focus en andere academische vaardigheden, kan je de workshop <a target='_blank' href='http://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-academisch-leren'>‘Smart study techniques’</a> or <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-academisch-leren'>‘Slim Studeren’</a> volgen.</li>
                        </ul>
                    "}
                    """
                }
            ),
            MockConstruct(
                name=valuing_name,
                construct_type=positive_trait_name,
                properties={
                    "norms": [73, 91],
                    "href": "https://thermos.sites.uu.nl/positive-motivationself-belief-learning-focus-and-valuing/#custom-collapse-0-2",
                    "feedback": "thermos.valuing.feedback",
                    "importance": "thermos.valuing.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        <li>Participating in the <a target='_blank' href='https://students.uu.nl/trainingen/training-transferable-skills'>‘Transferable skills’</a> training can provide insight in all the skills you have acquired during your studies, and why they are useful after graduation.</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        <li>Deelnemen aan de <a target='_blank' href='https://students.uu.nl/trainingen/training-transferable-skills'>‘Transferable skills’</a> training kan inzicht bieden in alle vaardigheden die je al hebt ontwikkeld tijdens je studie, en waarom die nutting zijn na je afstuderen.</li>
                        </ul>
                    "}
                    """
                }
            )
        ]),
        MockConstruct(name="Positive Engagement", construct_type=positive_trait_name, properties={}, children=[
            MockConstruct(
                name=persistence_name,
                construct_type=positive_trait_name,
                properties={
                    "norms": [60, 86],
                    "href": "https://thermos.sites.uu.nl/positive-engagement-persistence-planning-and-taskmanagement/#custom-collapse-0-0",
                    "feedback": "thermos.persistence.feedback",
                    "importance": "thermos.persistence.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        </ul>
                    "}
                    """
                }
            ),
            MockConstruct(
                name=planning_name,
                construct_type=positive_trait_name,
                properties={
                    "norms": [47, 79],
                    "href": "https://thermos.sites.uu.nl/positive-engagement-persistence-planning-and-taskmanagement/#custom-collapse-0-1",
                    "feedback": "thermos.planning.feedback",
                    "importance": "thermos.planning.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        <li>If you want help to further develop your planning skills, you can follow the workshop <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/workshop-timemanagement-en-uitstelgedrag'>'Kennismaken met Time management'</a> or the course <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-timemanagement-en-studeren'>‘Time management en studeren’</a> (both in Dutch).</li>
                        <li>Following the course <a target='_blank' href='https://students.uu.nl/agenda/training-bewust-effectief-werken-nederlandstalig'>‘Bewust en effectief werken’</a> could also add to this aspect’s development.</li>
                        <li>Participating in the course <a target='_blank' href='https://www.uu.nl/en/ecpd/workshop-smart-study-techniques-in-english'>‘Smart Study Techniques’</a> may also help.</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        <li>Als je graag hulp wilt bij het verder ontwikkelen van je planningsvaardigheden kan je de workshop <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/workshop-timemanagement-en-uitstelgedrag'>'Kennismaken met Time management'</a> of de cursus <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-timemanagement-en-studeren'>‘Time management en studeren’</a> volgen.</li>
                        <li>De workshop <a target='_blank' href='https://students.uu.nl/agenda/training-bewust-effectief-werken-nederlandstalig'>‘Bewust en effectief werken’</a> kan je ook helpen bij het ontwikkelen van je planningsvaardigheden.</li>
                        <li>Deelnemen aan de workshop <a target='_blank' href='https://www.uu.nl/en/ecpd/workshop-smart-study-techniques-in-english'>‘Smart Study Techniques’</a> kan ook helpen.</li>
                        </ul>
                    "}
                    """
                }
            ),
            MockConstruct(
                name=task_management_name,
                construct_type=positive_trait_name,
                properties={
                    "norms": [61, 85],
                    "href": "https://thermos.sites.uu.nl/positive-engagement-persistence-planning-and-taskmanagement/#custom-collapse-0-2",
                    "feedback": "thermos.task_management.feedback",
                    "importance": "thermos.task_management.importance",
                    "exercises": [],
                    "links":
                    """
                    {"en":"
                        <ul>
                        <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                        <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                        <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                        <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                        <li>You can take a look at the <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/publicaties/studietips'>‘Studietips’</a></li>
                        <li>If you want help to further develop your planning skills, you can follow the workshop <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/workshop-timemanagement-en-uitstelgedrag'>'Kennismaken met Time management'</a> or the course <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-timemanagement-en-studeren'>‘Time management en studeren’</a> (both in Dutch).</li>
                        <li>Following the course <a target='_blank' href='https://students.uu.nl/agenda/training-bewust-effectief-werken-nederlandstalig'>‘Bewust en effectief werken’</a> could also add to this aspect’s development.</li>
                        <li>Participating in the course <a target='_blank' href='https://www.uu.nl/en/ecpd/workshop-smart-study-techniques-in-english'>‘Smart Study Techniques’</a> may also help.</li>
                        </ul>
                    ",
                    "nl":"
                    <ul>
                        <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                        <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                        <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                        <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                        <li>Je kan kijken bij deze <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/publicaties/studietips'>‘Studietips’</a></li>
                        <li>Als je graag hulp wilt bij het verder ontwikkelen van je planningsvaardigheden kan je de workshop <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/workshop-timemanagement-en-uitstelgedrag'>'Kennismaken met Time management'</a> of de cursus <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/cursus-timemanagement-en-studeren'>‘Time management en studeren’</a> volgen.</li>
                        <li>De workshop <a target='_blank' href='https://students.uu.nl/agenda/training-bewust-effectief-werken-nederlandstalig'>‘Bewust en effectief werken’</a> kan je ook helpen bij het ontwikkelen van je planningsvaardigheden.</li>
                        <li>Deelnemen aan de workshop <a target='_blank' href='https://www.uu.nl/en/ecpd/workshop-smart-study-techniques-in-english'>‘Smart Study Techniques’</a> kan ook helpen.</li>
                        </ul>
                    "}
                    """
                }
            )
        ])
    ]),
    MockModel(name="GSQ", method="thermos_model", constructs=[
        MockConstruct(
            name=interpersonal_group_work_skills_name,
            construct_type=positive_trait_name,
            properties={
                "norms": [66, 86],
                "href": "https://thermos.sites.uu.nl/task-group-work-skills-and-interpersonal-group-work-skills/#custom-collapse-0-1",
                "feedback": "thermos.interpersonal_group_work_skills.feedback",
                "importance": "thermos.interpersonal_group_work_skills.importance",
                "exercises": [],
                "links":
                """
                {"en":"
                    <ul>
                    <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                    <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                    <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                    <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                    <li>Because the performance of a group involves taking into account the needs and opinions of every group member, being able to come to an equitable decision as efficiently as possible is important for the functioning of the group. There are a variety of ways to make decisions as a group. Try this <a target='_blank' href='https://uwaterloo.ca/centre-for-teaching-excellence/teaching-resources/teaching-tips/developing-assignments/group-work/group-decision-making'>seven-step decision-making model</a></li>
                    <li>Discussing what is important when working in a group can be done using the <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/wp-content/uploads/sites/475/2018/12/Matrix-Samenwerken_V4.pdf'>‘Matrix Samenwerken’</a> or the <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/wp-content/uploads/sites/475/2020/04/Collaboration-Grid.pdf'>‘Collaboration Grid’</a>. More info can be found on the <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/'>‘Samenwerkingsvragen’</a> page</li>
                    </ul>
                ",
                "nl":"
                <ul>
                    <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                    <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                    <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                    <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                    <li>Als een groep goed wil samenwerken is het belangrijk dat de mening van alle groepsleden gehoord wordt en dat er een beslissing wordt genomen waarin iedereen zich kan vinden. Dit proces is belangrijk voor het functioneren van een groep. Er zijn verschillende manieren om als groep beslissingen te maken, probeer eens dit <a target='_blank' href='https://uwaterloo.ca/centre-for-teaching-excellence/teaching-resources/teaching-tips/developing-assignments/group-work/group-decision-making'>seven-step decision-making model</a></li>
                    <li>Bespreken wat belangrijk is wanneer je samenwerkt kan met behulp van de <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/wp-content/uploads/sites/475/2018/12/Matrix-Samenwerken_V4.pdf'>‘Matrix Samenwerken’</a>. Meer informatie kan gevonden worden op de pagina <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/'>‘Samenwerkingsvragen’</a> page</li>
                    </ul>
                "}
                """
            }
        ),
        MockConstruct(
            name=task_group_work_skills_name,
            construct_type=positive_trait_name,
            properties={
                "norms": [58, 79],
                "href": "https://thermos.sites.uu.nl/task-group-work-skills-and-interpersonal-group-work-skills/#custom-collapse-0-0",
                "feedback": "thermos.task_group_work_skills.feedback",
                "importance": "thermos.task_group_work_skills.importance",
                "exercises": [],
                "links":
                """
                {"en":"
                    <ul>
                    <li>If you have any questions or concerns, you can talk to your tutor, study advisor, or career officer. The website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> and <a target='_blank' href='https://students.uu.nl/en/student-life/study-wellbeing-and-development/guidance-and-advice'>'guidance and advise'</a> may help determine whom to contact for certain questions.</li>
                    <li>You can join an <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> (in Dutch) from Onderwijsadvies & Training.</li>
                    <li>Consulting a <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> can help reduce study stress and add to the enjoyment of your study</li>
                    <li>Via the <a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a>, you can get in touch with a peer-coach to help your growth and development (Dutch and English)</li>
                    <li>Because the performance of a group involves taking into account the needs and opinions of every group member, being able to come to an equitable decision as efficiently as possible is important for the functioning of the group. There are a variety of ways to make decisions as a group. Try this <a target='_blank' href='https://uwaterloo.ca/centre-for-teaching-excellence/teaching-resources/teaching-tips/developing-assignments/group-work/group-decision-making'>seven-step decision-making model</a></li>
                    <li>Discussing what is important when working in a group can be done using the <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/wp-content/uploads/sites/475/2018/12/Matrix-Samenwerken_V4.pdf'>‘Matrix Samenwerken’</a> or the <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/wp-content/uploads/sites/475/2020/04/Collaboration-Grid.pdf'>‘Collaboration Grid’</a>. More info can be found on the <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/'>‘Samenwerkingsvragen’</a> page</li>
                    </ul>
                ",
                "nl":"
                <ul>
                    <li>Als je vragen hebt of je zorgen maakt kan je een gesprek aangaan met je tutor, studieadviseur, of career officer. De website <a target='_blank' href='https://students.uu.nl/naast-de-studie/studie-welzijn-en-ontwikkeling/begeleiding-en-advies'>'begeleiding en advies'</a> kan helpen bij het bepalen wie je kan helpen.</li>
                    <li>Je kan een <a target='_blank' href='https://www.uu.nl/onderwijs/onderwijsadvies-training/scholing/hoger-onderwijs/werken-aan-academische-vaardigheden/inloopspreekuur-academische-vaardigheden'>‘Online spreekuur’</a> bijwonen van Onderwijsadvies & Training.</li>
                    <li>Je kan een <a target='_blank' href='https://students.uu.nl/naast-de-studie/trainingen-skills-lab/studeercoaching'>Studycoach</a> raadplegen die je o.a. kan helpen om studiestress te verminderen en het plezier in studeren te vergroten.</li>
                    <li>Via de<a target='_blank' href='https://occ.sites.uu.nl/'>Online Coaching Center (OCC)</a> kun je in contact komen met een peer-coach die kan helpen met je groei en ontwikkeling (Nederlands en Engels)</li>
                    <li>Als een groep goed wil samenwerken is het belangrijk dat de mening van alle groepsleden gehoord wordt en dat er een beslissing wordt genomen waarin iedereen zich kan vinden. Dit proces is belangrijk voor het functioneren van een groep. Er zijn verschillende manieren om als groep beslissingen te maken, probeer eens dit <a target='_blank' href='https://uwaterloo.ca/centre-for-teaching-excellence/teaching-resources/teaching-tips/developing-assignments/group-work/group-decision-making'>seven-step decision-making model</a></li>
                    <li>Bespreken wat belangrijk is wanneer je samenwerkt kan met behulp van de <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/wp-content/uploads/sites/475/2018/12/Matrix-Samenwerken_V4.pdf'>‘Matrix Samenwerken’</a>. Meer informatie kan gevonden worden op de pagina <a target='_blank' href='https://samenwerkingsvragen.sites.uu.nl/'>‘Samenwerkingsvragen’</a> page</li>
                    </ul>
                "}
                """
            }
        )
    ])
]
#endregion constructs

#region thermos
thermos_questions = [
    MockQuestion(
      question_type="mc_1",
      body="""
        {"en":"
            My studyprogram is:
        ",
        "nl":"
            Ik studeer:
        "}
        """,
      required=False
    ),
    MockQuestion(
      question_type="mc_2",
      body="""
        {"en":"
            I'm currently enrolled in:
        ",
        "nl":"
            Ik zit in:
        "}
        """,
      required=False
    ),
    MockQuestion(
      question_type="mc_3",
      body="""
        {"en":"
            I identify as:
        ",
        "nl":"
            Ik identificeer me als:
        "}
        """,
      required=False
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            If I can't understand my university work at first, I keep going over it until I do.
        ",
        "nl":"
            Als ik mijn studiewerk niet gelijk snap, blijf ik doorgaan tot ik het snap
        "}
        """,
        construct_names=[persistence_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I feel very pleased with myself when I really understand what I'm taught at university.
        ",
        "nl":"
            Ik ben erg tevreden met mezelf als ik echt snap wat mij wordt geleerd op de universiteit
        "}
        """,
        construct_names=[learning_focus_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I study, I usually study in places where I can concentrate.
        ",
        "nl":"
            Als ik studeer doe ik dat meestal op plaatsen waar ik me kan concentreren
        "}
        """,
        construct_names=[task_management_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I'm able to use some of the things I learn at university in other parts of my life.
        ",
        "nl":"
            Ik kan dingen die ik leer aan de universiteit gebruiken in andere delen van mijn leven
        "}
        """,
        construct_names=[valuing_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Sometimes I don't try so hard at assignments so I have an excuse if I don't do so well.
        ",
        "nl":"
            Soms doe ik niet mijn best voor een opdracht zodat ik een excuus heb als ik het niet goed doe
        "}
        """,
        construct_names=[self_sabotage_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I don't do so well at university I'm often unsure how to avoid that happening again.
        ",
        "nl":"
            Als het niet goed gaat met studeren weet ik vaak niet hoe ik moet voorkomen dat het opnieuw mis gaat
        "}
        """,
        construct_names=[uncertain_control_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I feel very pleased with myself when I do well at university by working hard.
        ",
        "nl":"
            Ik ben erg tevreden met mezelf als ik door hard werken goed presteer op de universiteit
        "}
        """,
        construct_names=[learning_focus_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Each week I'm trying less and less.
        ",
        "nl":"
            Elke week doe ik minder mijn best
        "}
        """,
        construct_names=[disengagement_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            If an assignment is difficult, I keep working at it trying to figure it out.
        ",
        "nl":"
            Als een opdracht moeilijk is blijf ik eraan werken om het te snappen
        "}
        """,
        construct_names=[persistence_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When exams and assignments are coming up, I worry a lot.
        ",
        "nl":"
            Ik maak me veel zorgen als er examens en deadlines aankomen.
        "}
        """,
        construct_names=[anxiety_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Often the main reason I work at university is because I don't want people to think that I'm dumb.
        ",
        "nl":"
            Vaak is de belangrijkste reden om aan studieopdrachten te werken dat ik niet wil dat mensen denken dat ik dom ben.
        "}
        """,
        construct_names=[failure_avoidance_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I get a good mark I'm often not sure how I'm going to get that mark again.
        ",
        "nl":"
            Als ik een goed cijfer gehaald heb, weet ik vaak niet goed hoe ik  daarna opnieuw een goed cijfer kan krijgen.
        "}
        """,
        construct_names=[uncertain_control_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            If I try hard, I believe I can do my university work well
        ",
        "nl":"
            Ik geloof dat ik mijn studiewerk goed kan doen als ik hard mijn best doe
        "}
        """,
        construct_names=[self_belief_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Learning at university is important.
        ",
        "nl":"
            Studeren aan een universiteit is belangrijk
        "}
        """,
        construct_names=[valuing_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I don't really care about university anymore.
        ",
        "nl":"
            Ik geef eigenlijk niet meer om mijn opleiding
        "}
        """,
        construct_names=[disengagement_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I get a bad mark I'm often unsure how I'm going to avoid getting that mark again.
        ",
        "nl":"
            Als ik een slecht cijfer gehaald heb, weet ik vaak niet goed hoe ik kan voorkomen dat ik weer een slecht cijfer haal.
        "}
        """,
        construct_names=[uncertain_control_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I study, I usually organise my study area to help me study best.
        ",
        "nl":"
            Als ik studeer, organiseer ik mijn studie omgeving zodat ik optimaal kan studeren
        "}
        """,
        construct_names=[task_management_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I'm often unsure how I can avoid doing poorly at university.
        ",
        "nl":"
            Ik weet vaak niet zeker hoe ik kan voorkomen dat ik het slecht doe op de universiteit.
        "}
        """,
        construct_names=[uncertain_control_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I worry about failing exams and assignments.
        ",
        "nl":"
            Ik maak me zorgen over het niet halen van toetsen en opdrachten
        "}
        """,
        construct_names=[anxiety_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Often the main reason I work at university is because I don't want people to think bad things about me.
        ",
        "nl":"
            Vaak is de belangrijkste reden om aan studieopdrachten te werken dat ik niet wil dat mensen slecht over me denken
        "}
        """,
        construct_names=[failure_avoidance_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I get it clear in my head what I'm going to do when I sit down to study.
        ",
        "nl":"
            Ik zorg dat ik helder heb wat ik ga doen als ik ga studeren
        "}
        """,
        construct_names=[planning_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I've pretty much given up being involved in things at university.
        ",
        "nl":"
            Ik heb het grotendeels opgegeven om betrokken te zijn bij dingen van de universiteit
        "}
        """,
        construct_names=[disengagement_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            If I don't give up, I believe I can do difficult university work.
        ",
        "nl":"
            Ik geloof dat ik moeilijk studiewerk goed kan doen als ik niet op geef
        "}
        """,
        construct_names=[self_belief_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I sometimes don't study very hard before exams so I have an excuse if I don't do so well.
        ",
        "nl":"
            Soms studeer ik niet zo hard, zodat ik een reden heb als het tentamen niet zo goed gaat
        "}
        """,
        construct_names=[self_sabotage_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I feel very pleased with myself when what I learn at university gives me a better idea of how something works.
        ",
        "nl":"
            Ik ben erg tevreden met mezelf als ik beter snap hoe iets werkt door wat ik leer op de universiteit
        "}
        """,
        construct_names=[learning_focus_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I feel very pleased with myself when I learn new things at university.
        ",
        "nl":"
            Ik ben erg tevreden met mezelf als ik nieuwe dingen leer op de universiteit
        "}
        """,
        construct_names=[learning_focus_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Before I start an assignment, I plan out how I am going to do it.
        ",
        "nl":"
            Voordat ik een opdracht begin, plan ik hoe ik het ga aanpakken
        "}
        """,
        construct_names=[planning_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I'm taught something that doesn't make sense, I spend time to try to understand it.
        ",
        "nl":"
            Als mij iets wordt geleerd dat niet gelijk logisch is, besteed ik tijd om te proberen het te snappen
        "}
        """,
        construct_names=[persistence_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I've pretty much given up being interested in university.
        ",
        "nl":"
            Ik heb het grotendeels opgegeven om  geïnteresseerd te zijn in mijn opleiding
        "}
        """,
        construct_names=[disengagement_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I try to plan things out before I start working on my assignments.
        ",
        "nl":"
            Ik probeer een plan uit te denken voordat ik begin te werken aan een opdracht
        "}
        """,
        construct_names=[planning_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Often the main reason I work at university is because I don't want to disappoint others (eg. lecturers/family/partner).
        ",
        "nl":"
            Vaak is de belangrijkste reden om te studeren dat ik anderen (bijv. docenten/familie/partner) niet teleur wil stellen
        "}
        """,
        construct_names=[failure_avoidance_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I study, I usually try to find a place where I can study well.
        ",
        "nl":"
            Als ik studeer, probeer ik meestal een plek te kiezen waar ik goed kan studeren
        "}
        """,
        construct_names=[task_management_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            If I have enough time, I believe I can do well in my university work.
        ",
        "nl":"
            Ik geloof dat ik mijn studiewerk goed kan doen als ik genoeg tijd heb
        "}
        """,
        construct_names=[self_belief_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            What I learn at university will be useful in the future.
        ",
        "nl":"
            Wat ik leer aan de universiteit kan ik in de toekomst gebruiken
        "}
        """,
        construct_names=[valuing_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I sometimes do things other than study the night before an exam so I have an excuse if I don't do so well.
        ",
        "nl":"
            Soms doe ik andere dingen dan studeren de avond voor een examen, zodat ik een excuus heb als ik het niet goed doe
        "}
        """,
        construct_names=[self_sabotage_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I'll keep working at difficult university work until I think I've figured it out.
        ",
        "nl":"
            Ik blijf werken aan moeilijk studiewerk totdat ik het denk te snappen
        "}
        """,
        construct_names=[persistence_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I do test or exams I don't feel very good.
        ",
        "nl":"
            Als ik een toets of tentamen maak voel ik me niet goed
        "}
        """,
        construct_names=[anxiety_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Often the main reason I work at university is because I don't want my teacher/lecturer/tutor to think less of me.
        ",
        "nl":"
            Vaak is de belangrijkste reden om te studeren dat ik niet wil dat mijn docent of tutor slecht over me denkt
        "}
        """,
        construct_names=[failure_avoidance_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I usually stick to a study timetable or study plan.
        ",
        "nl":"
            Ik hou me normaal gesproken aan een timetable of studie-planning
        "}
        """,
        construct_names=[planning_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            If I work hard enough, I believe I can get on top of my university work.
        ",
        "nl":"
            Ik geloof dat ik mijn studiewerk op orde kan hebben als ik hard genoeg werk
        "}
        """,
        construct_names=[self_belief_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            It's important to understand what I'm taught at university.
        ",
        "nl":"
            Het is belangrijk dat ik begrijp wat me geleerd wordt aan de universiteit
        "}
        """,
        construct_names=[valuing_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            I sometimes put assignments and study off until the last moment so I have an excuse if I don't do so well.
        ",
        "nl":"
            Soms stel ik opdrachten en studeren uit tot het laatste moment zodat ik een excuus heb als ik het niet goed doe
        "}
        """,
        construct_names=[self_sabotage_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            In terms of my university work I'd call myself a worrier.
        ",
        "nl":"
            Als het gaat om het werk voor mijn studie zou ik mezelf een piekeraar noemen.
        "}
        """,
        construct_names=[anxiety_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            When I study, I usually study at times when I can concentrate best.
        ",
        "nl":"
            Als ik studeer, studeer ik meestal  op tijden waarop ik mij goed kan concentreren
        "}
        """,
        construct_names=[task_management_name]
    ),
    # Group part
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Provide emotional support to my group members.
        ",
        "nl":"
            Emotionele steun aan mijn groepsgenoten te geven.
        "}
        """,
        construct_names=[interpersonal_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Remind the group how important it is to stick to schedules.
        ",
        "nl":"
            De groep eraan te herinneren hoe belangrijk het is om ons aan de planning te houden.
        "}
        """,
        construct_names=[task_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Be sensitive to the feelings of other people.
        ",
        "nl":"
            Sensitief te zijn voor de gevoelens van mijn groepsgenoten.
        "}
        """,
        construct_names=[interpersonal_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Construct strategies from ideas that have been raised.
        ",
        "nl":"
            Strategieen te bedenken vanuit ideeën die geopperd zijn.
        "}
        """,
        construct_names=[task_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Show that I care about my group members.
        ",
        "nl":"
            Te laten zien dat ik geef om mijn groepsgenoten
        "}
        """,
        construct_names=[interpersonal_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Clearly define the roles of each group member.
        ",
        "nl":"
            De rollen van alle groepsleden helder te definiëren.
        "}
        """,
        construct_names=[task_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Be open and supportive when communicating with others.
        ",
        "nl":"
            Open en ondersteunend te zijn wanneer ik met anderen communiceer.
        "}
        """,
        construct_names=[interpersonal_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Move the group's ideas forward towards a strategy.
        ",
        "nl":"
            De ideeën van de groep verder te brengen tot een strategie.
        "}
        """,
        construct_names=[task_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Be there for other group members when they need me.
        ",
        "nl":"
            Er te zijn voor groepsgenoten wanneer zij mij nodig hebben.
        "}
        """,
        construct_names=[interpersonal_group_work_skills_name]
    ),
    MockQuestion(
        question_type="likert_7",
        body="""
        {"en":"
            Evaluate how well the group is progressing towards agreed goals.
        ",
        "nl":"
            De vooruitgang van de groep richting de afgesproken doelen te evalueren.
        "}
        """,
        construct_names=[task_group_work_skills_name]
    )
]

thermos_comments = [
    MockComment(
        body="""
        {"en":"
            When filling out this survey, you may note that some questions are quite similar.<br/>This is not a trick but the way these surveys work.<br/>Don't spend too long on each question, your first response is often a good one.
        ",
        "nl":"
            Wanneer je deze vragenlijst invult valt het je misschien op dat sommige vragen op elkaar lijken.<br/>Dat is geen truc, maar de manier waarop deze vragenlijsten werken.<br/>Besteed niet teveel tijd aan de vragen, want je eerste ingeving is vaak de juiste!
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            These questions are about working in groups during your study.<br/>When working in groups I tend to...
        ",
        "nl":"
            Deze vragen gaan over het werken in groepjes tijdens je studie.<br/>Als ik in een groep werk, dan heb ik de neiging om...
        "}
        """,
        location=44
    ),
]
#endregion thermos

#region thermos-feedback
thermos_feedback_questions = [
    MockQuestion(
        question_type="mc_1",
        body="""
        {"en":"
            My studyprogram is:
        ",
        "nl":"
            Ik studeer:
        "}
        """,
        required=False
    ),
    MockQuestion(
        question_type="mc_2",
        body="""
        {"en":"
            I'm currently enrolled in:
        ",
        "nl":"
            Ik zit in:
        "}
        """,
        required=False
    ),
    MockQuestion(
        question_type="mc_3",
        body="""
        {"en":"
            I identify as:
        ",
        "nl":"
            Ik identificeer me als:
        "}
        """,
        required=False
    ),
    MockQuestion(
        question_type="open",
        required=False,
        body="""
        {"en":"
            What is your general impression of the dashboard?
        ",
        "nl":"
            Wat is je algemene indruk van het dashboard?
        "}
        """
    ),
    MockQuestion(
        question_type="open",
        required=False,
        body="""
        {"en":"
            To what extent did you understand the different parts of the dashboard?
        ",
        "nl":"
            In hoeverre begreep je de onderdelen van het dashboard?
        "}
        """
    ),
    MockQuestion(
        question_type="open",
        required=False,
        body="""
        {"en":"
            To what extent are you able to apply what you learned in the dashboard?
        ",
        "nl":"
            In hoeverre kan je toepassen wat je hebt geleerd in het dashboard?
        "}
        """
    ),
    MockQuestion(
        question_type="open",
        required=False,
        body="""
        {"en":"
            Did your study behaviour change after using the dashboard? If so, how?
        ",
        "nl":"
            Is je studiegedrag veranderd na het gebruik van het dashboard? Zo ja, hoe?
        "}
        """
    ),
]
#endregion thermos-feedback

#region anxiety
anxiety_questions_1 = [
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    ),
]
anxiety_comments_1 = [
    MockComment(
        body="""
        {"en":"
            Before you deal with test anxiety, it might be important to learn how to relax. The good thing about relaxation is that anyone can learn how to do it and the more you practice it the better you get at it. There are many methods you can use to relax. In this exercise, you are going to try one.<br/><br/>(Do you remember your learning goal for Anxiety? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            Voordat je omgaat met zenuwen voor examens kan het belangrijk zijn om te leren ontspannen. Het mooie is dat iedereen kan leren ontspannen en hoe vaker je het oefent, hoe beter je erin wordt. Er zijn verschillende manieren die je kan gebruiken om te ontspannen. In deze oefening ga je er een proberen.<br/><br/> (Heb je je leerdoel voor Anxiety nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 1. Tell yourself that you are going to relax now.
        ",
        "nl":"
            Stap 1. Vertel jezelf dat je nu gaat ontspannen
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 2. Find somewhere quiet to sit or lie down.
        ",
        "nl":"
            Stap 2. Zoek een rustige plek om te zitten of te liggen
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 3. Make sure you are comfortable.
        ",
        "nl":"
            Stap 3. Zorg ervoor dat je comfortabel voelt
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 4. Concentrate on your breathing.<ul><li>Breathe deeply down into your belly</li><li>With your first in-breath count ‘one’ in your mind; with your second breath count ‘two’ and so on up to ‘five’ and then start again at ‘one’</li><li>As you breath out say ‘relaaaxxx’ in your mind</li></ul>
        ",
        "nl":"
            Stap 4. Concentreer je op je ademhaling.<ul><li>Adem diep in, in je buik</li><li>Met je eerste adem, tel ‘een’ in je hoofd, met je volgende adem ‘twee’, totdat je bij vijf bent. Begin dan weer bij een.</li><li>Wanneer je uitademt, zeg ‘relaaaax’ in je gedachten</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 5. After a few minutes of this you then progressively relax each part of your body.<ul><li>Focus on your right foot, clench the toes tightly for a few seconds and then slooooowwwly release them</li><li>Now do the same with your left foot </li><li>Now clench your right thigh muscles for a few seconds and then slowly release them</li><li>Now do the same with your left thigh muscles</li><li>Do the same with your right hand, left hand, stomach, and your face</li></ul>
        ",
        "nl":"
            Stap 5. Na een paar minuten dit gedaan te hebben, ga je gaandeweg elk onderdeel van je lichaam ontspannen.<ul><li>Focus eerst op je rechtervoet, span je tenen aan voor een paar seconde en laat ze heel langzaam weer los</li><li>Doe nu hetzelfde met je linkervoet </li><li>Span nu je rechterdijbeen aan voor een paar seconden en laat ze weer los</li><li>Doe nu hetzelfde voor je linkerdijbeen</li><li>Herhaal dit voor je rechterhand, linkerhand, buikspieren en je gezicht</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 6. Now your body is more relaxed, turn your mind to the most peaceful place you know. When your mind is there, take special notice of every part of that place and all the peaceful things about it.
        ",
        "nl":"
            Stap 6. Nu je lichaam meer ontspannen is, ga je met je gedachten naar de meest rustgevende plaats die je kent. Wanneer je daar in gedachten bent, probeer elk detail van die plek in je op te nemen en alle rustgevende elementen.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            If distracting thoughts enter your mind, that’s OK – focus back on your counting, body, or peaceful place.
        ",
        "nl":"
            Als afleidende gedachten in je opkomen dan is dat ok – focus rustig weer op het tellen, je lichaam, of je rustgevende plek.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 7. When you are ready, come back slowly – open your eyes slowly, flex your arms and legs, and get up slowly (you may feel a bit light headed, so don’t jump up).
        ",
        "nl":"
            Stap 7. Wanneer je er klaar voor bent, kom je langzaam weer terug. Open langzaam je ogen, strek je armen en benen, en sta rustig op ( je kan een beetje licht in je hoofd zijn, dus sta voorzichtig op)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Step 8. Set a day, time, and place for your next relaxation session
        ",
        "nl":"
            Stap 8. Plan alvast het volgende moment waarop je deze oefening wil herhalen
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            If this exercise doesn’t make you feel very good you may like to find another relaxation technique that suits you better
        ",
        "nl":"
            Als deze oefening je niet helpt, kan je natuurlijk op zoek naar een andere ontspanningsoefening.
        "}
        """,
        location=0
    )
]

anxiety_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {anxiety_name} 1: Relaxation in 15 minutes
        ",
        "nl":"
            {anxiety_name} 1: Ontspannen in 15 minuten
        "}}
        """,
    survey_type="action",
    construct_name=anxiety_name,
    questions=anxiety_questions_1,
    comments=anxiety_comments_1
)

anxiety_questions_2 = [
    MockQuestion(
        body="""
        {"en":"
            Which items do you need to pay special attention to - then add 3 more<br/><ul><li>Start your study early in term and do it regularly –but remember that late study is better than no study</li><li>Develop a study timetable and stick to it</li><li>Hand in all work on time</li><li>Look at past test papers; set your own test; hand in practice mini-essays (say, 250 words)</li><li>Write down the distractions that can arise leading up to an exam (eg. part-time work, friends). How will you deal with these?</li><li>Avoid making major life decisions before a test. Keep your relationships intact leading up to a test. Avoid the panickers leading up to and just before the exam. Also, avoid people who might unsettle or distract you in any way</li><li>Try to get good sleep in the week leading up to the exam. Not too much caffeine and a balanced diet in the week leading up to the exam. Leading up to the week of the test, try to do a bit of exercise to burn off excess anxiety</li><li>Practice your relaxation exercise when you can (see the previous exercise)</li><li>Look for teacher clues (material repeated in class; teacher says ‘this is on the test’; teacher asks class to take detailed notes)</li><li>Know the following: (a) material to be covered in test, (b) % of term/year mark allocated, (c) time allowed, (d) venue, (e) types of questions (multi-choice, essay, short answer, true/false etc), (f) marks for each section/question, (g) materials allowed in exam room</li></ul>
        ",
        "nl":"
            Kies welke manier jij extra aandacht wil geven, en verzin er nog drie bij.<br/><ul><li>Begin op tijd met studeren in het blok en studeer regelmatig, maar onthoud dat laat in het blok studeren altijd nog beter is dan niet studeren</li><li>Maak een studieschema en hou je daaraan</li><li>Lever al je werk ruim op tijd in</li><li>Kijk naar je vorige papers, maak je eigen oefententamens, lever mini-essays in (zeg, 250 woorden)</li><li>Schrijf de afleidingen op die kunnen voorkomen voor een tentamen (bijv. je bijbaan, vrienden). Hoe ga je om met die afleidingen?</li><li>Maak geen grote beslissingen vlak voor een tentamen</li><li>Hou je relaties intact in de aanloop naar een tentamen</li><li>Vermijd de paniekerige studenten voor en tijdens het tentamen. Vermijd ook de mensen waarbij je je niet op je gemakt voelt of die je afleiden.</li><li>Probeer genoeg slaap te krijgen in de week voor het tentamen</li><li>Drink niet te veel cafeïne, eet gezond en gevarieerd in de week voor het tentamen</li><li>Sporten of bewegen kan helpen stress verminderen in de week voor het tentamen</li><li>Doe de ontspanningsoefening wanneer je tijd hebt (zie Anxiety oefening 1)</li><li>Zoek naar tips van docenten (welk materiaal wordt benadrukt, of een docent zegt ‘dit komt op het tentamen, wanneer een docent vraag om goed op te letten)</li><li>Ken het volgende; a) welk materiaal er in het examen komt, b) de toegestane tijd, c) waar het is, d) het soort vragen (multiple choice, essay, open vragen), e) hoeveel punten je kan halen per onderdeel, f) wat je bij je mag hebben tijdens het tentamen.</li></ul>
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            How did this exercise help you working on your learning goal?
        "}
        """,
        question_type="open",
        required=False
    )
]
anxiety_comments_2 = [
    MockComment(
        body="""
        {"en":"
            Students who are well prepared for tests tend to be less anxious leading up to them and also less anxious while they are doing them. Too often students don’t prepare effectively for tests. This has the effect of increasing their anxiety leading up to and during the test. Remember, there are lots of ways to prepare eg. through study, looking at past papers, diet, and relaxation. In this exercise you will look at ways you can better prepare for tests. In the table below, tick the boxes you feel you need to pay particular attention to. Put this checklist on your wall at home, in your diary, or somewhere you will see it leading up to a test or exam. At the end of this list, add three more items.<br/><br/>(Do you remember your learning goal for Anxiety? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            Studenten die goed voorbereid zijn op tentamens zijn waarschijnlijk minder zenuwachtig van tevoren, en zijn ook minder zenuwachtig terwijl ze het tentamen maken. Het gebeurt nog erg vaak dat studenten niet goed voorbereiden voor tentamens. Dit kan weer leiden tot meer zenuwen voorafgaand en tijdens het tentamen. Onthoud dat er veel verschillende manieren zijn om voor te bereiden, bijvoorbeeld studiemateriaal doorkijken, artikelen doorlezen, ontspanningsoefeningen, en letten op wat je eet. In deze oefening ga je kijken hoe jij je beter kan voorbereiden op tentamens. Kies uit de lijst hieronder welke manieren jij extra aandacht wil geven. Schrijf ze op en hang ze zichtbaar op, schrijf ze in je dagboek, of ergens waar je het vaak tegenkomt voor een tentamen. Verzin tot slot nog 3 manieren waarmee jij aan je zenuwen wil werken. (Heb je je leerdoel voor Anxiety nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint.)
        "}
        """,
        location=0
    ),
]

anxiety_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {anxiety_name} 2: Preparing for tests
        ",
        "nl":"
            {anxiety_name} 2: Voorbereiden voor tentamens
        "}}
        """,
    survey_type="action",
    construct_name=anxiety_name,
    questions=anxiety_questions_2,
    comments=anxiety_comments_2
)

anxiety_questions_3 = [
    MockQuestion(
        body="""
        {"en":"
            Which ones do you need to pay special attention to - then add 3 more<br/><ul><li>If you’re a heavy sleeper, set two alarm clocks (out of reach from your bed) the night before the exam<li>Have all your materials ready the night before (including a watch)</li><li>Have breakfast. Arrive at the venue early</li><li>Avoid the panickers before the exam. Also avoid people who might unsettle or distract you in any way. If you’re easily distracted by other students, sit close to the front of the exam room (if you’re able to)</li><li>Read instructions very very very carefully. Know what marks are awarded to the test, how many sections/questions, allocate your time at the start</li><li>Look through the test paper so you know what’s ahead. Read questions very very very carefully –underline key words</li><li>For long answers, look back at the question frequently –this keeps you on-track</li><li>Pace yourself –know how much time is available for all the questions</li><li>For longer answers (eg. essays), spend 1 or 2 minutes at the start to sketch a quick answer plan</li><li>Take no notice of other students in the exam room</li><li>If you don’t know the answer to a question, don’t freak out; go onto another question and go back to the difficult question last –sometimes the answer comes to you as you’re doing another question</li><li>Know which method of test taking suits you (but be flexible depending on the exam): Do you prefer (a) working from the beginning to the end of the paper? (b) doing the easiest questions first? (c) doing mostdifficult questions first?</li><li>Write neatly</li><li>Use all the time available –if you finish early, check your answers</li></ul>
        ",
        "nl":"
            Welk van deze onderdelen kan of moet je extra aandacht geven?<br><ul><li>Als je moeilijk op kan staan, zet dan 2 wekkers (waar je niet vanuit bed bij kan) de avond voor een tentamen.</li><li>Leg alle materialen de avond voor het tentamen al klaar (inclusief een horloge)</li><li>Zorg dat je ontbijt</li><li>Kom ruim op tijd bij de plaats van het tentamen</li><li>Vermijd paniekerige medestudenten voor het examen. Vermijd ook de mensen waarbij je je ongemakkelijk voelt of die je afleiden</li><li>Als je snel afgeleid bent door andere studenten, ga dan vooral in de tentamen ruimte zitten (als dat kan)</li><li>Lees de instructies heel nauwkeurig</li><li>Weet hoe de becijfering van het tentamen werkt, hoeveel secties/vragen er zijn, en bedenk aan het begin hoeveel tijd je waaraan gaat besteden</li><li>Kijk het tentamen aan het begin een keer door, zodat je weet wat er nog aan komt</li><li>Lees de vragen heel nauwkeurig, onderstreep belangrijke woorden</li><li>Wanneer je een lang antwoord moet geven, kijk dan regelmatig weer even naar de vraag – zo blijf je op het juiste spoor met je antwoord</li><li>Bepaal voor jezelf een tempo – weet hoeveel tijd er ongeveer is per vraag</li><li>Voor langere antwoorden (bijv. een essay), neem in het begin 1 of 2 minuten de tijd om een overzicht of blauwdruk van je antwoord te maken</li><li>Negeer andere studenten in de tentamenruimte</li><li>Als je het antwoord op een vraag niet weet, raak dan niet in paniek. Ga door naar een andere vraag en kom als laatste terug bij die vraag – soms schiet het antwoord je te binnen wanneer je een andere vraag aan het beantwoorden bent</li><li>Weet welke manier van tentamens maken bij jou past (maar wees daar ook flexibel in afhankelijk van het examen): Past het bij jou om a) van het begin tot het eind door te werken? b) de makkelijkere vragen eerst te beantwoorden? C) De moeilijke antwoorden eerst te beantwoorden?</li><li>Schrijf netjes en duidelijk leesbaar</li><li>Gebruik de tijd die je hebt – als je eerder klaar bent, lees je antwoorden nog eens door</li></ul>
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
anxiety_comments_3 = [
    MockComment(
        body="""
        {"en":"
            Test taking is a skill that can be learnt. This skill significantly reduces anxiety you feel leading up to the test and  while  you  are  doing  the  test.  In this exercise you  will look  at  ways  you  can improve  your  test-taking skills. In the table below, tick the boxes you feel you need to pay particular attention to. Put this checklist on your  wall  at  home,  in  your  diary,  or  somewhere  you  will  see  it  the  night  before  a  test  or exam. At the end of this list add three more items.<br/><br/>(Do you remember your learning goal for Anxiety? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            Het maken van tentamens en examens is een vaardigheid die je kan leren. Deze vaardigheid kan het gevoel van Anxiety verminderen dat je hebt voor het tentamen of terwijl je het tentamen maakt. In deze oefening onderzoek je manieren waarop jij je tentamen-skills kan verbeteren. Hieronder zie je verschillende onderdelen waar je aandacht aan kan besteden. Hang deze checklist thuis ergens op, in je agenda, of ergens waar je het ziet de avond voor een tentamen. Voeg aan het eind van deze lijst nog 3 manieren toe.<br/><br/> (Heb je je leerdoel voor Anxiety nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    )
]

anxiety_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {anxiety_name} 3: Taking tests
        ",
        "nl":"
            {anxiety_name} 3: Examens en tentamens maken
        "}}
        """,
    survey_type="action",
    construct_name=anxiety_name,
    questions=anxiety_questions_3,
    comments=anxiety_comments_3
)

anxiety_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Learn how to relax quickly</li><li>Learn how to prepare effectively for tests</li><li>Learn how to take tests.</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leren om me gemakkelijk te ontspannen.</li><li>Leren hoe ik me beter kan voorbereiden voor tentamens of examens.</li><li>Leren hoe ik examens of tentamens kan maken. </li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
anxiety_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Anxiety has two parts: feeling nervous and worrying. Feeling nervous is the uneasy or sick feeling you get when you think about your university work, assignments, or exams. Worrying is your fear about not doing very well in your university work, assignments, or exams. If you are too anxious you tend to have difficulty concentrating, paying attention, and remembering things.
        ",
        "nl":"
            Anxiety heeft 2 belangrijke aspecten: zenuwachtig zijn en zorgen maken. Zenuwachtig zijn is het ongemakkelijke of misselijke gevoel dat je krijgt wanneer je denkt aan studieopdrachten of tentamens. Zorgen maken komt uit je angst om het niet goed te doen bij studieopdrachten of tentamens. Een beetje Anxiety kan nuttig zijn, maar teveel kan zorgen voor moeite met concentreren, je aandacht erbij houden, of dingen onthouden.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for reducing your Anxiety:<br/><ul><li>Learn to recognize the signs of anxiety. Some include feeling nervous, feeling sick in the stomach, having a racing heart, and worrying about failing</li><li>Learn some relaxation techniques that work for you. For example, practice deep breathing, gradually relax your muscles, and visualize entering the exam room, looking at the exam paper, and so on. There are some good books on relaxation.</li><li>Learn some practical ways to deal with what is making you anxious. This might include planning a study timetable, spending more time studying, starting assignments early, or not leaving study until the last minute</li><li>Focus on actually doing the assignment or exam question and not on thinking whether you might fail it</li><li>Practice working under exam conditions at home</li><li>Develop strategies for tests or exams. For example, focus only on one question. If you do not know the answer to that question, move on to another question and go back to it at the end.</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om Anxiety te verminderen:<br/><ul><li>Leer de signalen van Anxiety te herkennen bijvoorbeeld zenuwen, je misselijk voelen, een hoge hartslag hebben, of zorgen maken of je het wel gaat redden. </li><li>Leer een paar ontspanningsoefeningen die voor jou werken, bijvoorbeeld ademhalingstechnieken, geleidelijk je spieren ontspannen, of voorstellen dat je de tentamenzaal binnen loopt. Er bestaan goede boeken om je te helpen ontspannen.</li><li>Leer praktische manieren waarmee je om kan gaan met wat zenuwen veroorzaakt, bijv. een studieschema maken, meer tijd besteden aan studeren, eerder beginnen met opdrachten, en werk voor je studie niet uitstellen tot het laatste moment.</li><li>Focus op het daadwerkelijk maken van de opdracht of het examen, in plaats van denken of je het mogelijk niet gaat halen.</li><li>Oefen of studeer thuis onder dezelfde condities als het examen</li><li>Ontwikkel strategieën om tentamens of examens te maken. Bijvoorbeeld, focus op één vraag tegelijk. Als je het antwoord niet direct weet, ga dan door naar de volgende vraag en kom aan het einde terug.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for Anxiety. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Anxiety. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal: Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel: Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

anxiety_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare {anxiety_name}
        ",
        "nl":"
            Voorbereiden {anxiety_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=anxiety_name,
    questions=anxiety_questions_prepare,
    comments=anxiety_comments_prepare
)

anxiety_questions_reflect = [
    MockQuestion(
        body="""
        {"en":"
            Which of the last three Anxiety exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Anxiety oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'There are techniques you can learn to help you relax quickly' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Er zijn technieken die je kan leren om gemakkelijk te ontspannen’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'There are many ways to prepare effectively for tests' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Er zijn verschillende manieren om effectief voor te bereiden voor tentamens’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'Test-taking is a skill that can be learned' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Het maken van tentamens is een vaardigheid die je kan leren’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7", # !!!!!!!!!!!!! Not open
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Anxiety and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Anxiety, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open",
        required=False
    )
]
anxiety_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Anxiety Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “For History I’m going to do one practice test at home every week”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (bijv. “Voor vak X ga ik thuis elke week een oefententamen maken”)
        "}
        """,
        location=2
    )
]

anxiety_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {anxiety_name}
        ",
        "nl":"
            Reflecteren: {anxiety_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=anxiety_name,
    questions=anxiety_questions_reflect,
    comments=anxiety_comments_reflect
)

anxiety = [anxiety_1, anxiety_2, anxiety_3, anxiety_prepare, anxiety_reflect]
#endregion

#region failure_avoidance
failure_avoidance_questions_1 = [
    MockQuestion(
      question_type="open",
      body="""
        {"en":"
            What was your learning goal for Failure Avoidance? Describe below:
        ",
        "nl":"
            Wat was je leerdoel voor Failure Avoidance? Beschrijf deze hieronder:
        "}
        """,
      required=False
    ),
    MockQuestion(
      question_type="open",
      body="""
        {"en":"
            What is causing you most concern at university?<br/><i>(Eg. “I'm worried that I won't figure out how to do my Psychology assignment”)</i>
        ",
        "nl":"
            Wat veroorzaakt de meeste zorgen in je studie?<br/><i>(Eg.(Bijv. “Het baart me zorgen dat ik misschien niet weet hoe ik mijn Psychologie opdracht moet maken”) </i>
        "}
        """,
      required=False
    ),
    MockQuestion(
      question_type="open",
      body="""
        {"en":"
            <b>ACTION</b>: write down one thing that you can DO to start tackling the worry - provide details of how you
            will do this.<br/>(Eg. “I'll ask my teacher/lecturer if I have a problem or I'll spend more time at the library
            reading”)
        ",
        "nl":"
            <b>ACTION</b>: Schrijf een ding op dat jij kan DOEN om de zorgen te tackelen – geeft details over hoe je dat gaat doen.<br/>(bijv. “Ik ga mijn docent/tutor inschakelen als ik een probleem heb, of ik ga meer tijd besteden in de bibliotheek om te lezen”)
        "}
        """,
      required=False
    ),
    MockQuestion(
      question_type="open",
      body="""
        {"en":"
            <b>BELIEF</b>: Write down a short, <b>positive</b>, and strong statement about your belief in yourself to solve it.<br/>
            <i>(Eg. “I believe I can figure out a way to deal with this worry – all I need is time and effort”)</i>
        ",
        "nl":"
            <b>BELIEF</b>: Schrijf een kort, <b>positief</b>, a en sterk statement over jouw vertrouwen in jezelf om de zorgen op te lossen.<br/>
            <i>(bijv. “Ik vertrouw erop dat ik kan omgaan met deze zorgen – het kost alleen tijd en moeite”)</i>
        "}
        """,
      required=False
    ),
    MockQuestion(
      question_type="open",
      body="""
        {"en":"
            <b>COMMITMENT</b>: You may be more commited to solving a problem when you keep a goal in mind.
            Think about what is worrying you and write a realistic solution or outcome that you can aim for.<br/>
            (Eg. “I'll aim to spend as much time on the assignment as possible, will read widely, and think of
            different ways of solving problems as they arise”).
        ",
        "nl":"
            <b>COMMITMENT</b>: Als je een duidelijk doel voor ogen hebt is het waarschijnlijk makkelijker om een probleem op te lossen. Bedenk wat jouw zorgen baart en schrijf een realistische oplossing of uitkomst waar je voor kan gaan.<br/>
            (bijv. “Ik ga proberen om zoveel tijd te besteden aan de opdracht als nodig is, ga veel erover lezen, en verschillende manieren bedenken om problemen op te lossen als ze ontstaan”).
        "}
        """,
      required=False
    ),
    MockQuestion(
      question_type="open",
      body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
      required=False
    )
]
failure_avoidance_comments_1 = [
    MockComment(
        body="""
        {"en":"
            In this exercise you are going to tackle some of your fears. Fear can get in the way of your success
            and enjoyment at university. You can learn how to deal with your fear. Fear is the focus of this
            exercise because when fear underlies what students do, they may feel more anxious, less confident,
            and less control over their studies. Maybe you will see that by applying the following ABC technique (A
            = action, B = Belief, C = Commitment) your fears are not so overwhelming.
        ",
        "nl":"
            In deze oefening ga je aan de slag met een aantal van je angsten. Deze kunnen in de weg staan van studiesucces en of je plezier beleeft aan het studeren en je studie. Omgaan met een angst is iets wat je kan leren. Angst is de focus van deze oefening, omdat als dit de onderliggende reden is voor wat studenten doen, het kan leiden tot zenuwen en stress, gevoelens van onzekerheid, en minder controle over je studie. Als je de volgende ABC-techniek toepast (A = Action, B = Belief, C = Commitment), merk je misschien dat je angsten minder overweldigend zijn.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Failure Avoidance? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Failure avoidance nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    )
]

failure_avoidance_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {failure_avoidance_name} 1: The ABC of dealing with fear
        ",
        "nl":"
            {failure_avoidance_name} 1: Het ABC van omgaan met angst
        "}}
        """
    survey_type="action",
    construct_name=failure_avoidance_name,
    questions=failure_avoidance_questions_1,
    comments=failure_avoidance_comments_1
)

failure_avoidance_questions_2 = [
    MockQuestion(
        body="""
        {"en":"
            Describe a mistake you made on your university work recently –the bigger the mistake the better!! (eg. “I failed my History essay”)
        ",
        "nl":"
            Beschrijf een recente fout die je gemaakt hebt tijdens je studie – hoe groter hoe beter! (bijv. “Ik had een onvoldoende voor mijn paper.”)
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            What did you do or think that is under your control that led to that mistake? (eg. “I left it to the last minute so I rushed and didn’t read the question properly”)
        ",
        "nl":"
            Wat deed of dacht je dat leidde tot de fout waar je invloed op kan uitoefenen? (bijv. “Ik heb het uitgesteld tot het laatste moment en daarom de opdrachtomschrijving niet goed gelezen”)
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            What can you learn from this to improve next time? (eg. “I’ll get onto assignments earlier and I’ll read the question carefully next time”)
        ",
        "nl":"
            Wat kan je leren van deze fout zodat je het volgende keer beter kan doen? (bijv. “Ik ga eerder beginnen aan opdrachten en lees de opdrachtomschrijving goed door”).
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            See, now you have a better guide to success. By looking at your mistakes in this way you learn lessons that you can take into the next task to increase your chances of success.
        ",
        "nl":"
            Kijk, nu heb je een duidelijke richting naar succes. Door te kijken naar je fouten op een manier waarop je ervan leert, kan je het inzicht meenemen en de kans op succes in de toekomst vergroten.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
failure_avoidance_comments_2 = [
    MockComment(
        body="""
        {"en":"
            A major reason why students fear failure is because they believe it is the end of the world if they make a mistake. When  students  believe it is the end of the world to make amistake they focus on avoiding mistakes rather than being focused on personal bests, improving, or reaching for success. Students often forget that their mistakes can show them  where they can improve –mistakes can be the launch pad for success. The lessons learnt from mistakes are important for next time. You can take what you learnt last time to avoid making that mistake again. Therefore mistakes can be a powerful learning opportunity and not a statement about you as a person.
        ",
        "nl":"
            Een belangrijke reden waarom studenten bang zijn om te falen is omdat ze fouten zien als het einde van de wereld. Als studenten geloven dat dit zo is, focussen ze op het vermijden van fouten in plaats van op persoonlijke groei, verbeteringen of successen. Studenten vergeten vaak dat hun fouten ze kan laten zien waar ze kunnen verbeteren – fouten kunnen het startpunt zijn voor een verbeterproces. De lessen die je leert van gemaakte fouten kunnen belangrijk zijn in de toekomst, omdat je die les kan gebruiken om de fout niet nog eens te maken. Daarom kunnen fouten een belangrijke mogelijkheid om te leren zijn, niet een statement over jou als persoon.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Failure Avoidance? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Failure avoidance nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In this exercise you will see how mistakes can be the key to future improvement.
        ",
        "nl":"
            In deze oefening zal je zien hoe fouten de sleutel kunnen zijn voor verbetering in de toekomst.
        "}
        """,
        location=0
    )
]

failure_avoidance_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {failure_avoidance_name} 2: Mistakes can be the keys to my improvement
        ",
        "nl":"
            {failure_avoidance_name} 2: Fouten als sleutel voor mijn verbetering
        "}}
        """,
    survey_type="action",
    construct_name=failure_avoidance_name,
    questions=failure_avoidance_questions_2,
    comments=failure_avoidance_comments_2
)

failure_avoidance_questions_3 = [
    MockQuestion(
        body="""
        {"en":"
            Challenge the statement “The main reason I learn is because I don’t want to get bad marks” with a positive success focus
        ",
        "nl":"
            Tackle het statement “De belangrijkste reden om te leren is om geen slechte cijfers te halen” met een focus op positief succes.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Challenge the statement “The main reason I learn is because I don’t want people to think bad things about me” with a positive success focus
        ",
        "nl":"
            Tackle het statement “De belangrijkste reden om te leren is omdat ik niet wild at mensen slechte dingen over me denken” met een focus op positief succes.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Challenge the statement “The main reason I learn is because I don’t want to disappoint people” with a positive success focus
        ",
        "nl":"
            Tackle het statement “De belangrijkste reden om te leren is omdat ik mensen niet teleur wil stellen” met een focus op positief succes.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
failure_avoidance_comments_3 = [
    MockComment(
        body="""
        {"en":"
            When you do your university work mainly to avoid failing, to avoid the disapproval of others, or to not look ‘dumb’ it puts a lot of pressure on you as you learn. It  can  also  make  you  feel  quite anxious. These are ‘unhelpful’ reasons for learning. Instead we want to develop ‘helpful’ reasons for learning such as beating your personal bests, improving, and developing your skills.
        ",
        "nl":"
            Wanneer je studieopdrachten voornamelijk doet om falen te vermijden, afkeuring van anderen te vermijden, of om er niet ‘dom’ uit te zien, legt dat een hoop druk op je terwijl je studeert. Het kan je ook behoorlijk zenuwachtig maken. Dit zijn ‘onbehulpzame’ redenen om te leren. In plaats daarvan willen we ‘behulpzame’ redenen ontwikkelen om te leren, zoals persoonlijke groei, ontwikkeling, en verbetering.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In this  exercise you will tackle the ‘unhelpful’ reasons for learning. In the table below are some of the ‘unhelpful’ reasons you may have for learning. Your job is to challenge each one by writing out a more positive reason for learning
        ",
        "nl":"
            In deze oefening ga je de ‘onbehulpzame’ redenen om te leren tackelen. Hieronder zie je een aantal ‘onbehulpzame’ redenen die je misschien hebt om te leren. Aan jou de uitdaging om voor elke reden een nieuwe, positievere reden om te leren te omschrijven.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Failure Avoidance? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Failure avoidance nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            The more you can focus on the positive reasons for learning, the more you enjoy what you learn, the less anxious you are, and the better you’ll do.
        ",
        "nl":"
            Hoe meer je focust op positieve redenen om te leren, hoe meer plezier je hebt in wat je leert, hoe minder zenuwachtig je ervan wordt, en hoe beter je het doet.
        "}
        """,
        location=3
    )
]

failure_avoidance_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {failure_avoidance_name} 3: Tackling the 'unhelpful' reasons for learning
        ",
        "nl":"
            {failure_avoidance_name} 3: Tackle de 'onbehulpzame' reden om te leren
        "}}
        """,
    survey_type="action",
    construct_name=failure_avoidance_name,
    questions=failure_avoidance_questions_3,
    comments=failure_avoidance_comments_3
)

failure_avoidance_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Look at how you may get in the way of your own success.</li><li>Look at reasons why you get in the way of your own success.</li><li>Find ways to remove obstacles to your success.</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Manieren leren waarmee je kan omgaan met je angst of zorgen.</li><li>Leren inzien hoe een fout of een vergissing het startpunt voor success kan zijn.</li><li>Leren hoe je een positievere insteek naar je studie kan innemen.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
failure_avoidance_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            You are failure avoidant when you do your university work mainly to avoid failure (rather than to aim for success or improvement) or to avoid people’s disapproval or disappointment. If you are failure avoidant, you tend to fear failure, feel pessimistic, and feel anxious when thinking about or doing your university work.
        ",
        "nl":"
            Failure avoidance houdt in dat je studieopdrachten voornamelijk doet om te voorkomen dat je het slecht doet, in plaats van streven naar succes of verbetering. Of, dat je wil voorkomen dat het eruit ziet alsof je het slecht doet. Ook ben je waarschijnlijker bang om te falen, voel je je pessimistisch, of voel je je zenuwachtig wanneer je studeert of aan je studie denkt.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for reducing your failure avoidance:<br/><ul><li>Focus on achieving personal bests and improving more than trying to avoid doing poorly or to avoid the disapproval of others.</li><li>Recognize that your mistakes tell you where you went wrong and what areas you can improve. Mistakes can be the launch pad for success.</li><li>Understand that with hard work and effective study you can achieve personal bests and not be so worried about doing poorly.</li><li>Be proud of yourself when you do your best and try your hardest no matter what your mark is or what people say or think about your results.</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om Failure avoidance te verminderen:<br/><ul><li>Focus op het bereiken van je eigen streefdoelen, in plaats van foccussen op het vermijden van slechte resultaten of de afkeuring van anderen.</li><li>Probeer je fouten of vergissingen te zien als mogelijkheden om te verbeteren. Fouten en vergissingen kunnen het startpunt zijn van succes.</li><li>Begrijp dat je door hard te werken en effectief te studeren je eigen streefdoelen kan behalen, en dat je niet druk hoeft te maken over mogelijk falen.</li><li>Wees trots op jezelf wanneer je hard werkt en je best doet, los van de beoordeling of wat anderen ervan vinden.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for failure avoidance. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor failure avoidance. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel.<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

failure_avoidance_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {failure_avoidance_name}
        ",
        "nl":"
            Voorbereiden: {failure_avoidance_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=failure_avoidance_name,
    questions=failure_avoidance_questions_prepare,
    comments=failure_avoidance_comments_prepare
)

failure_avoidance_questions_reflect = [
    MockQuestion(
        body="""
        {"en":"
            Which of the last three Failure avoidance exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Failure avoidance oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'You can learn how to deal with fears you have about your university work and tests' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Je kan leren omgaan met je angsten over studieopdrachten en examens.’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'Mistakes can be the launch pad to improvement' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Fouten kunnen het startpunt zijn van een leerproces’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'Try to focus on improving or achieving success more than avoiding failure' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Probeer te focussen op verbeteren of je doel bereiken, in plaats van falen te vermijden’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7",  # !!!!!!!!!!!!! Not open
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Failure avoidance and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Anxiety, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open",
        required=False
    )
]
failure_avoidance_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “On my next essay I’ll focus on doing a good job and not on whether I’ll fail it”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (bijv. “Bij mijn volgende essay focus ik op het goed doen, en niet of ik het wel ga halen”).
        "}
        """,
        location=2
    )
]

failure_avoidance_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {failure_avoidance_name}
        ",
        "nl":"
            Reflecteren: {failure_avoidance_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=failure_avoidance_name,
    questions=failure_avoidance_questions_reflect,
    comments=failure_avoidance_comments_reflect
)

failure_avoidance = [failure_avoidance_1, failure_avoidance_2, failure_avoidance_3, failure_avoidance_prepare, failure_avoidance_reflect]
#endregion

#region uncertain_control
uncertain_control_questions_1 = [
    MockQuestion(
        body="""
        {"en":"
            Provide a list of reasons why you've done well in the past
        ",
        "nl":"
            Beschrijf de redenen dat je het in het verleden goed hebt gedaan
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Provide a list of reasons why you haven't done so well in the past
        ",
        "nl":"
            Beschrijf de redenen dat je het in het verleden niet goed  hebt gedaan
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
uncertain_control_comments_1 = [
    MockComment(
        body="""
        {"en":"
            The first step in building your sense of control can be looking at the reasons why you’ve done well or not so well in the past. In the table below you are asked to list all the reasons why you’ve done well or not so well.
        ",
        "nl":"
            De eerste stap voor het opbouwen van je gevoel van controle op je studie is het zoeken naar redenen waarom je het eerder wel of niet goed hebt gedaan. Hieronder beschrijf je de redenen waarom het in het verleden wel of niet goed ging.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Things to think about include:<br/><ul><li>Hard work or lack of work</li><li>Good luck or bad luck</li><li>Easy test or difficult test</li><li>Test or study conditions (eg. uncomfortable chairs, weather too hot etc)</li><li>Arrived early or late</li><li>Well prepared or not so well prepared</li><li>Asked teacher/lecturer/tutor for help or didn’t ask for help etc</li></ul>
        ",
        "nl":"
            Denk daarbij na over:<br/><ul><li>Hard werken of een gebrek daaraan</li><li>Geluk of ongeluk</li><li>Makkelijke of moeilijke tentamens</li><li>Studie-omstandigheden (te warm, geluidsoverlast, etc.)</li><li>Te vroeg of te laat arriveren</li><li>Hoe goed je voorbereid was</li><li>Of je om hulp hebt gevraagd van bijv. een docent</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Uncertain control? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Uncertain control nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise you are going to look at which of the reasons you are in your control.
        ",
        "nl":"
            In de volgende oefening ga je kijken op welk van deze oefeningen je invloed kan uitoefenen.
        "}
        """,
        location=2
    )
]

uncertain_control_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {uncertain_control_name} 1: Why I've done well or not so well in the past
        ",
        "nl":"
            {uncertain_control_name} 1: Waarom ik het eerder wel of niet goed deed
        "}}
        """,
    survey_type="action",
    construct_name=uncertain_control_name,
    questions=uncertain_control_questions_1,
    comments=uncertain_control_comments_1
)

uncertain_control_questions_2 = [
    MockQuestion(
        body="""
        {"en":"
            Provide the list of reasons why you've done well and add whether or not you are in control
        ",
        "nl":"
            Beschrijf de redenen waarom je het goed hebt gedaan, en hoe je daar controle over had.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Provide the list of reasons why you haven't done so well and add whether or not you are in control
        ",
        "nl":"
            Beschrijf de redenen waarom je het niet goed hebt gedaan, en of je daar controle over had.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
uncertain_control_comments_2 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Uncertain Control? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Uncertain control nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the last exercise you listed reasons why you have done well or not so well in the past. In this exercis e you are going to look at which of these are <u>in your control</u>. Things are in your control when there is something you can do to change them. For example, the amount of study you do is in your control because you can increase how much you do or reduce how much you do. However, the difficulty of a test is <u>not in your control</u> because it’s up to the teacher/lecturer/tutorand you cannot change it.
        ",
        "nl":"
            In de vorige oefening heb je de redenen beschreven waarom je het in het verleden wel of niet goed hebt gedaan. In deze oefening ga je kijken op welk van die redenen je controle hebt, dus waar jij invloed op kan uitoefenen en kan veranderen. Hoeveel je studeert is iets waar je invloed op kan uitoefenen, omdat je dat meer of minder kan doen. Op de moeilijkheid van een tentamen kan je geen invloed uitoefenen omdat die gemaakt wordt door de docenten.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the questions below, write out the list from the previous  exercise. Next to each item in your list, write ‘Control’ next to the things you can controlor change. Write the word ‘No’ next to things you can’t control or change. Don’t worry if you have no ‘Control’ words in your questions, you will develop some ‘Control’ words in the next exercise!
        ",
        "nl":"
            Beschrijf hieronder de lijst uit de vorige oefening. Beschrijf ook voor elk onderdeel van de lijst of je daar controle op hebt of kan veranderen. In de volgende oefening ga je kijken hoe je controle kan uitoefenen.
        "}
        """,
        location=0
    )
]

uncertain_control_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {uncertain_control_name} 2: What I can control
        ",
        "nl":"
            {uncertain_control_name} 2: Waar heb ik controle op
        "}}
        """,
    survey_type="action",
    construct_name=uncertain_control_name,
    questions=uncertain_control_questions_2,
    comments=uncertain_control_comments_2
)

uncertain_control_questions_3 = [
    MockQuestion(
        body="""
        {"en":"
            Provide a list of reasons why you've done well that were in your control
        ",
        "nl":"
            Maak een lijst met redenen waar jij invloed op had, die hebben bijgedragen aan een goede prestatie of een goed cijfer
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Provide a list of reasons why you haven't done so well in the past, but were in your control
        ",
        "nl":"
            Maak een lijst met redenen waar jij invloed op had, die hebben bijgedragen aan een slechte prestatie of een slecht cijfer
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Think of 3 more controllable things
        ",
        "nl":"
            Bedenk nu zelf nog 3 dingen waar je controle op hebt:
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
uncertain_control_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Uncertain Control? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Uncertain control nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            As much as possible you need to focus on things you can  control. When you focus on things you can control you feel  more confident and tend to do better in your studies. In this exercise you are going to focus on all the things in your control. Look back at the previous exercise and write in the questions below all the items with the word ‘Control’ beside them. The more you focus on these the more confident and in control you will feel.
        ",
        "nl":"
            Probeer zoveel mogelijk te focussen op dingen waar je controle op hebt. Als je focust op dingen waar je controle over hebt, ben je waarschijnlijk zelfverzekerder en doe je het vaak beter in je studie. In deze oefening ga je focussen op de dingen waar je controle op hebt. Kijk terug naar de vorige oefening en schrijf hieronder alle onderdelen waarop je controle had. Hoe meer je focust op deze onderdelen, hoe meer controle je hebt over je studieverloop.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Here is a list of things that all students can control and which lead to success at university.<br/><ul><li>Amount of Study</li><li>Preparation for tests and exams</li><li>Test-taking skills</li><li>Study tehcniques</li><li>Asking lecturers for help</li><li>Attitude towards university</li><li>Visiting the library</li><li>Organizing your study conditions</li><li>Presentation of your work</li><li>Avoiding distractions</li><li>Not wasting time</li><li>Doing your relaxation practice</li></ul>
        ",
        "nl":"
            Hier is een lijst van onderwerpen waar studenten controle over hebben en die leiden tot meer succes in je studie: <br/><ul><li>Hoeveel je studeert</li><li>Je studeertechnieken</li><li>Hoe vaak je de bibliotheek bezoekt</li><li>Afleidingen vermijden</li><li>Voorbereiden voor tentamens</li><li>Docenten om hulp vragen</li><li>Studie-omstandigheden verbeteren</li><li>Geen tijd verspillen</li><li>Tentamenvaardigheden verbetren</li><li>Attitude t.o.v. de universiteit veranderen</li><li>Presenteren van je werk</li><li>Ontspanningsoefeningen doen</li></ul>
        "}
        """,
        location=2
    ),
    MockComment(
        body="""
        {"en":"
            All these are the sorts of things you need to focus on in the future. These all increase your control over the marks you get
        ",
        "nl":"
            Dit zijn allemaal onderdelen waar jij je op kan focussen in de toekomst, en hebben een invloed op de cijfers die je haalt.
        "}
        """,
        location=2
    )
]

uncertain_control_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {uncertain_control_name} 3: Keys to my control
        ",
        "nl":"
            {uncertain_control_name} 3: Sleutel tot controle
        "}}
        """,
    survey_type="action",
    construct_name=uncertain_control_name,
    questions=uncertain_control_questions_3,
    comments=uncertain_control_comments_3
)

uncertain_control_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Learn to identify why you have done well or not so well in the past.</li><li>Learn to identify what things in your study and university.</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leer identificeren waarom je het goed of juist niet zo goed deed in het verleden.</li><li>Leer identificeren welke dingen je in je studie wel kan controleren en daaraan werken.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
uncertain_control_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            You are uncertain in control when you are unsure about how to do well or how to avoid doing poorly. If you are uncertain in control you can feel somewhat helpless when doing your university work, fear failure, and have negative thoughts about your university work.
        ",
        "nl":"
            Uncertain control is wanneer je niet zeker weet hoe je het goed kan doen in je studie, of kan vermijden het slecht te doen. Met hoge uncertain control voel je je misschien wat hulpeloos als je studeert, ben je bang om te falen, en heb je negatieve gedachten over je studie.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for increasing your control:<br/><ul><li>Recognize the aspects of your study that you can control and develop these. Aspects of study that you can control include your hard work, the way you study, and to some extent your study conditions.</li><li>Recognize that you may not always do as well as you would like but understand that hard work and studying well are the ingredients for doing better more often.</li><li>Do regular revision and study. Some study every day builds control and success.</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om uncertain control te verminderen:<br/><ul><li>Herken de aspecten van je studie waar je controle over kan hebben en ontwikkel deze. Dit kan bijvoorbeeld zijn hoe hard je werkt, de manier waarop je studeert, en in bepaalde mate de condities waarin je studeert.</li><li>Begrijp dat je misschien niet altijd zo goed presteert als je zou willen, maar dat hard werken en studeren de ingredienten zijn om het beter te doen.</li><li>Probeer regelmatig te studeren, elke dag een beetje zorgt voor controle en succes.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for self-sabotage. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Anxiety. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel.<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

uncertain_control_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {uncertain_control_name}
        ",
        "nl":"
            Voorbereiden: {uncertain_control_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=uncertain_control_name,
    questions=uncertain_control_questions_prepare,
    comments=uncertain_control_comments_prepare
)

uncertain_control_questions_reflect = [
    MockQuestion(
        body="""
        {"en":"
            Which of the last three Uncertain control exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Uncertain control oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'It is first important to know why you have done well or not so well in the past' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Het is eerst belangrijk om te weten waarom je het eerder niet zo goed deed’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'Then it is important to focus on what things in your study and university life you can control' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Daarna is het belangrijk om te focussen op wat je kan doen om controle te krijgen over je studie’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7",  # !!!!!!!!!!!!! Not open
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Uncertain control and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Uncertain control, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open",
        required=False
    )
]
uncertain_control_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Uncertain control Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst. <br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “On difficult university work, I’ll think about ways I’ve got through tough work before”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Voor moeilijke studieopdrachten denk ik aan manieren waarmee ik dat eerder heb opgelost”)
        "}
        """,
        location=2
    )
]

uncertain_control_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {uncertain_control_name}
        ",
        "nl":"
            Reflecteren: {uncertain_control_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=uncertain_control_name,
    questions=uncertain_control_questions_reflect,
    comments=uncertain_control_comments_reflect
)

uncertain_control = [uncertain_control_1, uncertain_control_2, uncertain_control_3, uncertain_control_prepare, uncertain_control_reflect]
#endregion

#region self_sabotage
self_sabotage_questions_1 = [
    MockQuestion(
        body="""
        {"en":"
            List three of the main ways you may get in the way of your own success
        ",
        "nl":"
            Beschrijf de drie belangrijkse manieren waarop jij je eigen succes in de weg zit.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
self_sabotage_comments_1 = [
    MockComment(
        body="""
        {"en":"
            The first step in overcoming self-sabotage and becoming more success focused may be to recognize ways you might get in the way of your own success.
        ",
        "nl":"
            De eerste stap in het overwinnen van self-sabotage en meer gefocust worden op je successen is het herkennen van manieren waarop jij je eigen succes in de weg zit
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the next exercise you will look at reasons why you might do this; then you will look at how to address it.
        ",
        "nl":"
            In de volgende oefening kijk je naar de redenen waarom je dit misschien doet, daarna kijk je hoe je ze kan overwinnen.
        "}
        """,
        location=1
    )
]

self_sabotage_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {self_sabotage_name} 1: How I get in the way of my own success
        ",
        "nl":"
            {self_sabotage_name} 1: Hoe ik mijn eigen succes in de weg sta
        "}}
        """,
    survey_type="action",
    construct_name=self_sabotage_name,
    questions=self_sabotage_questions_1,
    comments=self_sabotage_comments_1
)

self_sabotage_questions_2 = [
    MockQuestion(
        body="""
        {"en":"
            In the questions below, copy your answers given in the previous exercise and for each item write down the reasons you think you do this OR write down what benefits it might have.
        ",
        "nl":"
            Kopieer hieronder je antwoord van de vorige opdracht. Beschrijf voor elk onderdeel welke reden eronder zit, OF beschrijf wat de voordelen hiervan zijn.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
self_sabotage_comments_2 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Self-Sabotage? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Self-sabotage nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the last exercise you focused on the ways you get in the way of your own success. In this exercise you will take a close and honest look at the reasons why you might do this.
        ",
        "nl":"
            In de vorige oefening lag de focus op hoe jij je eigen succes in de weg zit, in deze oefening kijk je eerlijk en kritisch naar de reden waarom je dit doet.
        "}
        """,
        location=0
    )
]

self_sabotage_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {self_sabotage_name} 2: Why I get in the way of my own success
        ",
        "nl":"
            {self_sabotage_name} 2: Waarom ik mijn eigen succes in de weg sta
        "}}
        """,
    survey_type="action",
    construct_name=self_sabotage_name,
    questions=self_sabotage_questions_2,
    comments=self_sabotage_comments_2
)

self_sabotage_questions_3 = [
    MockQuestion(
        body="""
        {"en":"
            Copy your answers to the previous exercise into the field below and challenge each reason with an optimistic and committed alternative way of looking at your university work
        ",
        "nl":"
            Kopieer je antwoord van oefening 2 hieronder en geef voor elk onderdeel een tegenargument. Geef hierin een optimistische, alternatieve manier om naar je studie en studieopdrachten te kijken.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
self_sabotage_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Self-Sabotage? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Self-sabotage nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the last exercise you focused on the reasons why you may get in the way of your own success. In this exercise you will look at ways you can challenge these reasons – when you challenge the reasons you are challenging  the  obstacles  themselves.
        ",
        "nl":"
            In deze vorige oefening lag de focus op de reden waarom je in de weg kan staan van je eigen succes. In deze oefening kijk je naar manieren om die uitdagingen te overwinnen – als je de redenen achter de uitdaging aanpakt, pak je ook het obstakel
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            The more you are able to (a) recognize the obstacles to your success, (b) identify the reasons for these obstacles, and (c) challenge these reasons, the more you will enjoy university and perform better.
        ",
        "nl":"
            Hoe meer je in staat bent om a) obstakels naar succes te herkennen, b) onderliggende redenen te herkennen, en c) deze te kunnen omvormen, hoe meer plezier je hebt bij het studeren en hoe beter je het waarschijnlijk zult doen.
        "}
        """,
        location=1
    )
]

self_sabotage_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {self_sabotage_name} 3: Removing obstacles to my success
        ",
        "nl":"
            {self_sabotage_name} 3: Obstakels naar succes wegnemen
        "}}
        """,
    survey_type="action",
    construct_name=self_sabotage_name,
    questions=self_sabotage_questions_3,
    comments=self_sabotage_comments_3
)

self_sabotage_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Look at how you may get in the way of your own success.</li><li>Look at reasons why you get in the way of your own success.</li><li>Find ways to remove obstacles to your success.</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Verkennen of en hoe jij je eigen succes in de weg kan zitten. </li><li>Kijken naar redenen waarom jij je eigen success in de weg zit. </li><li>Manieren vinden om obstakels tot success te overwinnen.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
self_sabotage_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Self-sabotage is doing things that reduce your success at university. Examples are putting off doing an assignment or wasting time while you are meant to be studying for an exam. If you’re self-sabotage you tend not to make the most of your ability, do not feel so good about being at university, and tend not to achieve as highly as you are able.
        ",
        "nl":"
            Self-sabotage is dingen doen die je succes op de universiteit verminderen, zoals het uitstellen van studeren of tijdverspillen terwijl je zou moeten studeren voor een tentamen. Met hoog self-sabotage maak je waarschijnlijk niet optimaal gebruik van je capaciteiten, voel je je niet heel goed over je studie, en presteer je niet zo goed als je zou willen.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for reducing your self-sabotage:<br/><ul><li>Make a list of subjects in which you think you self-sabotage. How do you think and feel about these subjects?<ul><li>If you find them too competitive, read the section on ‘learning focus’</li><li>If you feel very anxious when you study for them, read the section on ‘anxiety’</li><li>If you think that no matter how hard you try you cannot do well in them, read the section on ‘low control’</li><li>If you are frightened of failing them, read the section on ‘failure avoidance’</li></ul></li><li>Understand that your worth as a person does not depend on the mark you get. What counts are doing your best and working hard.</li><li>Recognize that your mistakes tell you where you went wrong and what areas you can improve. Mistakes can be the launch pad for success</li><li>Try to focus on doing the best you can and improving on previous marks and try not to focus on your shortcomings or how you compare with others</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u>om self-sabotage te verminderen:<br/><ul><li>Maak een lijst van dingen waarin jij self-sabotage herkent, hoe voel je je over die dingen?<ul><li>Als ze gaan over gevoelens van competitive, kijk dan bij ‘learning focus’</li><li>Als ze gaan over gevoelens van zenuwen en zorgen maken, kijk dan bij ‘anxiety’</li><li>Als je denkt dat je geen controle over die dingen hebt, kijk dan bij ‘uncertain control’</li><li>Als je bang bent dat je die dingen niet gaat halen, kijk dan bij ‘failure avoidance’</li></ul></li><li>Probeer te begrijpen dat jouw waarde als person niet afhangt van het cijfer dat je krijgen. Wat ertoe doet is je best doen.</li><li>Herken dat je fouten indicaties zijn voor waar iets mis is gegaan, en dat het een startpunt kan zijn voor verbetering.</li><li>Probeer te verbeteren in je studie door te vergelijken met je eigen prestaties in plaats van de competitie met anderen aangaan.</li><li>Probeer te focussen op je best doen en vooruitgang ten opzichte van vorige presentatie, niet op je tekortkomingen, of hoe je het doet in vergelijking met anderen.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for self-sabotage. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Anxiety. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel.<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

self_sabotage_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {self_sabotage_name}
        ",
        "nl":"
            Voorbereiden: {self_sabotage_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=self_sabotage_name,
    questions=self_sabotage_questions_prepare,
    comments=self_sabotage_comments_prepare
)

self_sabotage_questions_reflect = [
    MockQuestion(
        body="""
        {"en":"
            Which of the last three Self-sabotage exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Self-sabotage oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'Be aware of the times that you may get in the way of your own success.' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Wees bewust wanneer van de keren dat jij jezelf in de weg hebt gezeten’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'Look closely and honestly at reasons why you get in the way of your own success.' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Kijk eerlijk naar redenen waarom jij jezelf in de weg kan zitten.’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How does the message 'There are ways you can remove the obstacles to your success' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Er zijn manieren om de obstakels tot success te verwijderen’ bij jou?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7",  # !!!!!!!!!!!!! Not open
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Self-sabotage and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Self-sabotage, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open",
        required=False
    )
]
self_sabotage_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Self-sabotage Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “tend to waste time when I’m meant to be studying for statistics tests. From now on I’ll make an effort to spend quality time on study when these tests are coming up”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Ik verspil vaak tijd wanneer ik eigenlijk zou moeten studeren voor een examen. Vanaf nu ga ik proberen om de tijd nuttig te besteden als er een examen aan komt”)
        "}
        """,
        location=2
    )
]

self_sabotage_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {self_sabotage_name}
        ",
        "nl":"
            Reflecteren: {self_sabotage_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=self_sabotage_name,
    questions=self_sabotage_questions_reflect,
    comments=self_sabotage_comments_reflect
)

self_sabotage = [self_sabotage_1, self_sabotage_2, self_sabotage_3, self_sabotage_prepare, self_sabotage_reflect]
#endregion

#region disengagement
disengagement_questions_1 = [
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: spend a bit more time studying at night. How much extra time?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Iets meer tijd besteden aan studeren. Hoeveel extra tijd?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: study in a place where I can concentrate. Where?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Studeren op een plek waar je je kan concentreren. Waar?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: study at times when I can concentrate. When?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Studeren op een tijdstip wanneer jij je goed kan concentreren. Welk tijdstip?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: learn how to write better essays and reports. Who can you ask for help/advice?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Leren hoe je betere essays of papers schrijft. Wie kan je vragen om hulp of advies?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: ask a teacher/lecturer for help if I have  problems with my university work. Who can you ask?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Een docent/tutor om hulp vragen als je problemen hebt met je studieopdracht. Wie kan je vragen?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: spend a bit more time doing assignments or study in a subject I’m having trouble in. What subjects?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Iets meer tijd besteden aan oefeningen of onderdelen waar je moeite mee hebt. Welke oefening(en)?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: ask a teacher for feedback about how to improve my assignments. What specific question will you ask?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Een docent om feedback vragen over hoe jij je opdrachten beter kan doen. Welke specifieke vraag stel je?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: check I’m on track when answering questions (eg. re-read essay question as I go). In what subjects?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Kijken of je op de juiste weg bent wanneer je vragen beantwoord (bijv. tentamenvragen nog een keer lezen terwijl je het tentament maakt). Voor welke vak(ken)?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: keep trying even when things are difficult. In what subjects do you might tend to give up a bit too soon?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Doorzetten, zelfs wanneer opdrachten moeilijk zijn. Wanner heb je de neiging om iets te snel op te geven?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Things you can do to have a say in how you perform: listen more carefully in class and ask questions if I don’t understand (either during or after class). In what subjects?
        ",
        "nl":"
            Wat je kan doen om het iets beter te doen in je studie: Goed luisteren tijdens hoorcolleges of werkgroepen en vragen stellen wanneer je iets niet snapt (tijdens of erna). Voor welke onderdelen?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het bereiken van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
disengagement_comments_1 = [
    MockComment(
        body="""
        {"en":"
            You have a say in how you do at university. There are almost always some things that you can do to influence the results you get and how much you enjoy university. In this exercise, you’ll look at some things that you can do to perform a bit better at university and to enjoy university more. As you read each one, answer the associated question.<br/><br/>(Do you remember your learning goal for Disengagement? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            Jij bepaalt voor het grootste gedeelte hoe je het doet in je studie aan de universiteit. Er is bijna altijd iets dat je kan doen om je resultaten te verbeteren en hoe je studeren ervaart. In deze oefening kijk je naar een aantal dingen die je kan doen om het ietsje beter te doen in je studie en om er meer plezier uit te halen. Terwijl je de statements leest, beantwoord dan de vraag die daarbij hoort.<br/><br/> (Herinner jij je leerdoel voor Disengagement nog? Als dat niet zo is, lees die dan weer even terug voordat je deze oefening maakt.)
        "}
        """,
        location=0
    )
]

disengagement_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {disengagement_name} 1: I have a say in how I do at university
        ",
        "nl":"
            {disengagement_name} 1: Ik bepaal hoe ik het doe in mijn studie
        "}}
        """,
    survey_type="action",
    construct_name=disengagement_name,
    questions=disengagement_questions_1,
    comments=disengagement_comments_1
)

disengagement_questions_2 = [
    MockQuestion(
        body="""
        {"en":"
            I improved in one part of a subject (eg. improved my statistics, essay writing, note-taking)
        ",
        "nl":"
            Ik ben beter geworden in 1 onderdeel van een vak (bijv. beter geworden in statistiek, schrijven van een essay, of notities maken).
        "}
        """,
        question_type="mc_yes_no", # !!!!!!!!!!!!! Not open
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Completed all my assignment
        ",
        "nl":"
            Al mijn opdrachten gemaakt
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I contributed to class discussion
        ",
        "nl":"
            Ik heb bijgedragen aan een groepsdiscussie
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I enjoyed a lesson (or two!)
        ",
        "nl":"
            Ik vond een vak (of twee!) leuk
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I turned up to a class I didn’t really want to go to and stayed the whole lesson
        ",
        "nl":"
            Ik ben naar een vak geweest waar ik niet naartoe wilde en ben de hele tijd gebleven
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I didn’t give up on a uni work problem that was difficult
        ",
        "nl":"
            Ik heb niet opgegeven bij een moeilijke studieopdracht
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I did everything a teacher/lecturer asked me to
        ",
        "nl":"
            Ik heb alles gedaan wat een docent me vroeg
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I helped one of my friends with their study
        ",
        "nl":"
            Ik heb een van mijn vrienden geholpen met studeren
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I presented my university work neatly
        ",
        "nl":"
            Ik heb mijn studieopdrachten netjes gepresenteerd
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I got really interested in a lesson
        ",
        "nl":"
            Ik was echt geïnteresseerd in een vak of opdracht
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I got a nice comment or compliment from a teacher/lecturer
        ",
        "nl":"
            Ik heb een mooi compliment of opmerking gekregen van een docent of tutor
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I completed an assignment that I didn’t really want to do
        ",
        "nl":"
            Ik heb een opdracht afgemaakt waar ik echt geen zin in had
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I checked my work before handing it in
        ",
        "nl":"
            Ik heb mijn opdracht gecheckt voordat ik het inleverde
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I answered a question in class
        ",
        "nl":"
            Ik heb een vraag beantwoord in een hoor- of werkcollege
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I turned up to a class I didn’t really want to go to
        ",
        "nl":"
            Ik was bij een vak waar ik echt niet naartoe wilde
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I asked a teacher/lecturer for help
        ",
        "nl":"
            Ik heb een docent of tutor om hulp gevraagd
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I went to the library to find some extra reading for an assignment or university work
        ",
        "nl":"
            Ik ben naar de bibliotheek gegaan om wat extra te lezen voor een opdracht
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I tried a new way of studying to improve the way I study
        ",
        "nl":"
            Ik heb een nieuwe manier van studeren geprobeerd om mijn studiegedrag te verbeteren
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I double-checked my grammar
        ",
        "nl":"
            Ik heb mijn spelling gedubbelcheckt
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I did some extra uni work I wasn’t required to do
        ",
        "nl":"
            Ik heb wat extra’s gedaan voor mijn studie
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I thought university wasn’t too bad
        ",
        "nl":"
            Ik vond studeren eigenlijk best ok
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            I worked well in a group
        ",
        "nl":"
            Ik heb goed samengewerkt
        "}
        """,
        question_type="mc_yes_no",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Now write in 2 more things you did OK at in the last 2 weeks
        ",
        "nl":"
            Schrijf nu 2 dingen op die je ook OK hebt gedaan in de afgelopen 2 weken.
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het bereiken van je leerdoel?
        "}
        """,
        question_type="open",
        required=False
    )
]
disengagement_comments_2 = [
    MockComment(
        body="""
        {"en":"
            Even when things at university look bad and you think lots of things are going badly for you, there are usually some things in your life that aren’t so bad. Sure, they might not be perfect, but they’re not dreadful.  Recognizing  these  not-so-bad things is called ‘glimpsing’. Glimpsing some OK things in your university life  is clear  evidence  that  things  can  be  OK.  When  you  realize  that  things  in  your university life can be OK, you have good reason to be more optimistic. In this exercise you will identify some OK things that have happened recently. Tick which ones you have done in the last 2 weeks –then add 2 more OK things you have done<br/><br/>(Do you remember your learning goal for Disengagement? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            Zelfs wanneer het er voor je studie niet goed uit ziet en er veel dingen mis gaan, komt er een moment in je leven dat je je realiseert dat het leven zo slecht nog niet is. Natuurlijk ging het niet perfect, maar het was ook niet verschrikkelijk. Het herkennen van deze toch-best-ok onderdelen in je studie is bewijs dat dingen OK kunnen zijn. Wanneer je je realiseert dat onderdelen van je studie en leven als student OK kunnen zijn, heb je een goede reden om optimistischer te zijn. In deze oefening ga je een paar toch-best-ok onderdelen identificeren die recent zijn gebeurd. Klik aan welke je in de laatste 2 weken hebt gedaan, en voeg 2 toch-best-ok onderdelen toe.<br/><br/>(Herinner jij je leerdoel voor Disengagement nog? Als dat niet zo is, lees die dan weer even terug voordat je deze oefening maakt.)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            What were OK things in the last 2 weeks?
        ",
        "nl":"
            Wat waren toch-best-ok dingen van de afgelopen 2 weken?
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            These are small examples of how you, university work, teachers/lecturers, and university can be OK. Sure, they don’t happen all the time –but if they happened once they can happen twice and if they happen twice they can happen three times –and so on.
        ",
        "nl":"
            Dit zijn kleine voorbeelden van hoe jij, studieopdrachten, docenten en tutoren, en je studie OK kunnen zijn. Deze gebeuren natuurlijk niet allemaal de hele tijd, maar als ze eens gebeurd zijn kan dat nog een keer voorkomen, en een derde keer, etc.
        "}
        """,
        location=23
    )
]

disengagement_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {disengagement_name} 2: Glimpsing the past - When things weren't so bad
        ",
        "nl":"
            {disengagement_name} 2: Terugkijken naar het verleden – wanneer ging het beter.
        "}}
        """,
    survey_type="action",
    construct_name=disengagement_name,
    questions=disengagement_questions_2,
    comments=disengagement_comments_2
)

disengagement_questions_3 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Write 4 OK things from the previous exercise (Disengagement 2) and write how you are going to make them happen in the next 2 weeks
        ",
        "nl":"
            Schrijf 4 toch-best-ok onderdelen uit Disengagement 2 op, en hoe je dit gaat realiseren.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het bereiken van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
disengagement_comments_3 = [
    MockComment(
        body="""
        {"en":"
            In the previous exercise you glimpsed some  of the OK things that happened over the last 2 weeks. An important way to be more confident in the future is through taking some of these OK things and looking at  how  you  can  make  them  happen  again  in  the  next  2  weeks.  Here,  you  will  look  at  the  previous exercise (Disengagement 2) and pick 4 things you can make happen in the next 2 weeks and say how you are going to make them happen.<br/><br/>(Do you remember your learning goal for Anxiety? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            In de vorige oefening heb je gekeken naar toch-best-ok onderdelen die in de afgelopen 2 weken zijn gebeurd. Een belangrijke manier om meer vertrouwen te hebben in de toekomst is door deze onderdelen mee kan nemen naar de toekomst, en ervoor te zorgen dat deze weer gebeuren de komende tijd. Hier kijk je naar welke 4 onderdelen je van de Disengagement 2 oefening wil laten gebeuren in de komende 2 weken.<br/><br/>(Herinner jij je leerdoel voor Disengagement nog? Als dat niet zo is, lees die dan weer even terug voordat je deze oefening maakt.)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            As you can see, there are ways you can make some of the OK things happen again in your life in the next 2 weeks.
        ",
        "nl":"
            Zoals je kan zien is er altijd wel iets dat je kan doen om deze onderdelen te laten gebeuren in je leven.
        "}
        """,
        location=1
    )
]

disengagement_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {disengagement_name} 3: Glimpsing at the future
        ",
        "nl":"
            {disengagement_name} 3: Vooruitkijken naar de toekomst
        "}}
        """,
    survey_type="action",
    construct_name=disengagement_name,
    questions=disengagement_questions_3,
    comments=disengagement_comments_3
)

disengagement_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Learn to look at how you have a say in how you do at university</li><li>Learn to look at some good things that have happened at university recently</li><li>Learn to identify some ways you can make some good things happen at university in the next two weeks</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leren zien hoe jij invloed kan hebben op hoe je het doet in je studie.</li><li>Leren zien welke dingen er al wel goed gaan in je studie.</li><li>Leer manieren waarmee je binnen 2 weken positieve dingen voor je studie kan bereiken.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    )
]
disengagement_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Disengagement is where you feel like giving up in particular university subjects or university generally. Students who score highly in disengagement are more likely to believe there is little they can do to avoid failure or to repeat or attain success. Disengaged students are less likely to be interested in university or university work.
        ",
        "nl":"
            Disengagement is het gevoel van opgeven op een bepaald onderwerp op de universiteit of studeren in het algemeen. Studenten die hoog scoren op disengagement geloven vaker dat er weinig tot niets is dat zij kunnen doen om falen te voorkomen of juist te slagen. Voor deze studenten is het minder waarschijnlijker dat geïnteresseerd zijn in hun studie.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for reducing your Disengagement:<br/><ul><li>Understand that you are not helpless. You control how much study you do as well as the quality of that study, who you study with, and what you study</li><li>Try to see things in terms of shifts – small positive changes in your life are examples of success</li><li>Try to ‘glimpse’ good things that happen in your university life – that is, recognize some of the OK things about university or your university work and tell yourself that if they happen once they can happen again</li><li>Don’t lose hope – through the above steps and other exercises in this workbook you can make some positive shifts in your life. You are not stuck where you are if you want to turn things around</li><li>Identify someone who can help and encourage you – when you ask for help or advice you are no longer on your own. This could be a teacher, family member, counselor, or a friend who can provide some good help with your university work and how you are thinking and feeling about things.</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om Disengagement te verminderen:<br/><ul><li>Begrijp dat je niet hulpeloos bent. Jij hebt controle over je studie, hoeveel moeite je ervoor doet, hoe goed je het doet, met wie je studeert en wat je studeert.</li><li>Probeer dingen te zien in termen van veranderingen – kleine positieve veranderingen in je leven of je studie zijn voorbeelden van succes.</li><li>Probeer te herkennen welke aspecten van je studie ok of goed gaan. Overtuig jezelf dat als dat een keer gelukt is, dat het vaker kan lukken. </li><li>Geef de moed niet op – door deze tips en andere oefeningen in dit dashboard kan je positieve veranderingen maken in je leven. Je zit niet vast waar je nu bent en je kan dingen veranderen.</li><li>Zoek iemand die je kan helpen en je kan aanmoedigen – als je om hulp vraagt sta je er niet langer alleen voor. Dit kan een docent zijn, iemand uit je familie, een studieadviseur of tutor, of een vriend die je kan ondersteunen met je studie en hoe je daarover denkt.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for Disengagement. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Disengagement. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel:<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

disengagement_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {disengagement_name}
        ",
        "nl":"
            Voorbereiden: {disengagement_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=disengagement_name,
    questions=disengagement_questions_prepare,
    comments=disengagement_comments_prepare
)

disengagement_questions_reflect = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Which of the last three Disengagement exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Disengagement oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'You are in control of lots of things in your university life' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Je hebt heel veel controle over dingen die in je studie en studentenleven gebeuren.’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Some (even 1 or 2) OK things have happened at uni in the last 2 weeks' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘In de afgelopen 2 weken zijn er toch-best-ok dingen gebeurd (al is het er maar 1 of 2). ’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'You can make some OK things happen at university in the next 2 weeks' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Je kan toch-best-ok dingen realiseren in de komende 2 weken van je studie.’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Disengagement and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Disengagement, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open"
    )
]
disengagement_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Disengagement Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “I can make some good things happen in the next 2 weeks at uni/college. For example, to get interested in a lesson I can concentrate, not talk to my friends, and take some notes”)
        ",
        "nl":"
             Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (bijv. “ik ga toch-best-ok onderdelen realiseren in de komende 2 weken van mijn studie.”).
        "}
        """,
        location=2
    )
]

disengagement_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {disengagement_name}
        ",
        "nl":"
            Reflecteren: {disengagement_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=disengagement_name,
    questions=disengagement_questions_reflect,
    comments=disengagement_comments_reflect
)

disengagement = [disengagement_1, disengagement_2, disengagement_3, disengagement_prepare, disengagement_reflect]
#endregion

#region self_belief
self_belief_questions_1 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List 3 hindering thoughts about the project or test, then write down something that challenges each thought, finally write down a new helping thought to replace the old thought
        ",
        "nl":"
            Noem 3 belemmerende gedachten over het project, opdracht of tentamen, beschrijf daarna het bewijs tegen die gedachten, en schrijf nieuwe gedachten om de oude te vervangen.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    ),
]
self_belief_comments_1 = [
    MockComment(
        body="""
        {"en":"
            You increase your self-belief through positive thinking. Students who are low in self-belief tend to think negatively about themselves and what they do. In this exercise you will identify some hindering thoughts, look at evidence that can challenge these hindering thoughts, and look at some other ways of thinking that can increase your self-belief.
        ",
        "nl":"
            Je kan je Self-belief verhogen door positief te denken. Studenten die een lage mate van self-belief hebben, hebben de neiging om negatiever te denken over zichzelf en wat ze doen. In deze oefening ga je belemmerende gedachten leren herkennen, kijken naar het bewijs daartegen, en andere manieren van kijken die je self-belief kunnen verhogen.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Self-belief? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Self-belief nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Think about an upcoming project, assignment, or test that may be concerning you and complete the following questions.
        ",
        "nl":"
            Denk aan een project, opdracht, of tentamen in de nabije toekomst waar je je zorgen over maakt, en vul deze vraag in
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Next time you think about an assignment or test in a negative way, remember to (a) identify the hindering thought, (b) think of some evidence to challenge this hindering thought, and (c) use this evidence to develop a helping thought.
        ",
        "nl":"
            De volgende keer dat je nadenkt over een opdracht of tentamen op een negatieve manier, onthoud dan om a) de belemmerende gedachte te herkennen, b) bewijs te vinden tegen die gedachte, en c) dat te gebruiken om een behulpzame gedachte te ontwikkelen.
        "}
        """,
        location=1
    )
]

self_belief_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {self_belief_name} 1: Changing how I think
        ",
        "nl":"
            {self_belief_name} 1: Veranderen hoe ik denk
        "}}
        """,
    survey_type="action",
    construct_name=self_belief_name,
    questions=self_belief_questions_1,
    comments=self_belief_comments_1
)

self_belief_questions_2 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In my last assignment I did these things:
        ",
        "nl":"
            Bij mijn vorige opdracht heb ik deze dingen gedaan en deze stappen ondernomen:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
self_belief_comments_2 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Self-Belief? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Self-belief nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            To build or maintain your self-belief it is important to recognize that we don’t often give ourselves credit for all the successes in our lives. For example, we don’t recognize that in doing an assignment we achieve many successes along the way.
        ",
        "nl":"
            Om je self-belief op te bouwen of te onderhouden is het belangrijk om te herkennen dat we onszelf niet altijd de waardering geven voor de successen in ons leven. We herkennen bijvoorbeeld niet dat het doen van een opdracht ons in de toekomst succes kan opleveren.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In this exercise you are going to identify the many ways you succeed in doing an assignment. Think about the last assignment or project you completed. List the steps involved in completing that assignment or project. Think about whether you went to the library, surfed the Internet, prepared a plan, talked to lecturers/tutors, summarized main points, read some books, wrote a rough draft etc. If you did any of these things, write them in the question below – these are all small successes that you achieved along the way (you don’t have to list all 16 things – just as many as you can think of).
        ",
        "nl":"
            In deze oefening ga je de manieren waarop jij succes kan hebben in een opdracht leren herkennen. Denk aan de laatste opdracht of het laatste project dat je hebt afgemaakt. Beschrijf de stappen die nodig waren om het af te ronden. Bedenk of je naar de bibliotheek bent gegaan, op internet hebt gezocht, een plan hebt gemaakt, met docenten hebt gepraat, een samenvatting op hoofdpunten hebt gemaakt, boeken hebt gelezen, een eerste ruwe versie hebt geschreven, etc. Als je iets van deze dingen hebt gedaan, beschrijf die dan hieronder – het zijn kleine successen die je gaandeweg hebt behaald (je hoeft ze niet allemaal op te schrijven, zoveel als jij kan bedenken).
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Next time you do an assignment or study for a test, remember to give yourself credit for all the steps you completed along  the  way  before handing in your assignment or doing the test. By  doing this, you immediately build success into your life even before you getyour mark for that assignment or test. When you recognize these successes you have every reason to feel good about yourself
        ",
        "nl":"
            De volgende keer dat je een opdracht maakt of voor een tentamen studeert, onthoud dan dat je jezelf waardering geeft voor alle stappen die je hebt gezet. Door dit te doen, bouwen je succeservaringen in je leven in, zelfs voordat je een cijfer voor een tentamen of opdracht hebt gekregen. Als je je successen herkent heb je genoeg reden om tevreden te zijn met jezelf.
        "}
        """,
        location=1
    )
]

self_belief_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {self_belief_name} 2: Building more success into my life
        ",
        "nl":"
            {self_belief_name} 2: Succes inbouwen in je leven
        "}}
        """,
    survey_type="action",
    construct_name=self_belief_name,
    questions=self_belief_questions_2,
    comments=self_belief_comments_2
)

self_belief_questions_3 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 1
        ",
        "nl":"
            Talent 1
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 2
        ",
        "nl":"
            Talent 2
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 3
        ",
        "nl":"
            Talent 3
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 4
        ",
        "nl":"
            Talent 4
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 5
        ",
        "nl":"
            Talent 5
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 6
        ",
        "nl":"
            Talent 6
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 7
        ",
        "nl":"
            Talent 7
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Talent 8
        ",
        "nl":"
            Talent 8
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
self_belief_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Self-Belief? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Self-belief nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Another important way to build your self-belief is to be fully aware of your talents. Too often we do not recognize our talents.
        ",
        "nl":"
            Nog een belangrijke manier om aan je self-belief te bouwen is je bewust te worden van je talenten. Wij erkennen onze talenten lang niet vaak genoeg.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <b>WE ALL HAVE TALENTS</b>
        ",
        "nl":"
            <b>WE HEBBEN ALLEMAAL TALENTEN</b>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In this exercise you MUST list 8 university-related talents. Throw modesty out the window.
        ",
        "nl":"
            In deze oefening MOET je minimaal 8 studiegerelateerde talenten beschrijven, en wees daarbij niet te bescheiden.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            These are your talents and are the keys to your success<ul><li>Write them out in large print</li><li>Put them in your diary</li><li>Pin them on your wall at home</li><li>Even memorize them</li></ul>
        ",
        "nl":"
            Dit zijn jouw talenten en kunnen de sleutel zijn naar succes.<ul><li>Druk ze op groot formaat af</li><li>Schrijf ze op in je agenda</li><li>Hang ze thuis op</li><li>Leer ze zelfs uit je hoofd.</li></ul>
        "}
        """,
        location=8
    ),
]

self_belief_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {self_belief_name} 3: Talent Scout
        ",
        "nl":"
            {self_belief_name} 3: Talenten zien
        "}}
        """,
    survey_type="action",
    construct_name=self_belief_name,
    questions=self_belief_questions_3,
    comments=self_belief_comments_3
)

self_belief_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Learn how to challenge your negative thinking and learn how to think more positively</li><li>Learn to identify the many ways you succeed as you do your university work</li><li>Learn to identify your university-related talents and strengths</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leer je negatieve gedachtes uit te dagen en positiever te denken</li><li>Leer je successen te herkennen in je studie</li><li>Leer je je talenten en sterke kanten te herkennen.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
self_belief_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Self-belief is your belief and confidence in your ability to understand or to do well in your university work, to meet challenges you face, and to perform to the best of your ability. If you have a positive self- belief you tend to do difficult university work confidently, feel optimistic, try hard, and enjoy university.
        ",
        "nl":"
            Self belief is, als het gaat over studeren, het geloof en vertrouwen in je eigen vermogen om het goed te doen op de universiteit, uitdagingen in je studie aan te gaan, leermogelijkheden aan te grijpen en op je beste kunnen te presteren. Met veel self-belief doe je moeilijke studieopdrachten met meer zelfvertrouwen, voel je je optimistischer, probeer je harder, en beleef je meer plezier aan studeren.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for developing a self-belief:<br/><ul><li>Become more aware of negative thoughts you may have about yourself or events in your life, take time to look for evidence that challenges these negative thoughts, and develop more positive ways to think about things using this challenging evidence</li><li>Recognize all your successes as you do your university work. For example, break an assignment into smaller parts and be pleased with yourself for completing each part</li><li>Recognize improvements you make, trying not to focus on your shortcomings. If you do not do so well, focus on how you can learn from that to improve</li><li>Learn how to recognize your talents – yes, everyone has talents – and learn how to use them to your advantage</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om Self-belief te ontwikkelen:<br/><ul><li>Word bewust van negatieve gedachtes die je mogelijk hebt over je zelf of gebeurtenissen in je leven. Neem de tijd om naar bewijs te zoeken tegen die negatieve gedachten en ontwikkel een positievere kijk met behulp van dat bewijs </li><li>Herken je successen wanneer je studeert. Je kan bijvoorbeeld opdrachten opdelen in behapbare stukken, en blij zijn wanneer je elk onderdeel af hebt.</li><li>Herken de verbeteringen die je maakt, probeer niet te focussen op je tekortkomingen. Als het even niet zo goed gaat, probeer daarvan te leren en het als startpunt voor verbetering te zien.</li><li>Leer je talenten herkennen – ja, iedereen heeft talenten – en leer hoe je die kan inzetten voor jouw voordeel.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for Self belief. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Self belief. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel:<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

self_belief_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {self_belief_name}
        ",
        "nl":"
            Voorbereiden: {self_belief_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=self_belief_name,
    questions=self_belief_questions_prepare,
    comments=self_belief_comments_prepare
)

self_belief_questions_reflect = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Which of the last three Self-belief exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Self-belief oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Tackle negative thinking with evidence so as to develop more positive thoughts' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Tackle negatieve gedachten met bewijs, zodat je positievere gedachten ontwikkeld.’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Identify the many ways you succeed as you do your university work' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Herken de manieren waarop jij succesvol bent tijdens in je studieopdrachten’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Get to know your university-related talents and strengths' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Leer wat je sterke kanten zijn in je studie’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Self belief and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Self-belief, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open"
    )
]
self_belief_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Self-belief Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “Every time I think I can’t do something I’ll remember times I’ve been successful”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Elke keer als ik denk dat het niet gaat lukken, herriner ik mezelf aan de keren dat het wel gelukt is”)
        "}
        """,
        location=2
    )
]

self_belief_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {self_belief_name}
        ",
        "nl":"
            Reflecteren: {self_belief_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=self_belief_name,
    questions=self_belief_questions_reflect,
    comments=self_belief_comments_reflect
)

self_belief = [self_belief_1, self_belief_2, self_belief_3, self_belief_prepare, self_belief_reflect]
#endregion

#region learning_focus
learning_focus_questions_1 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Identify a subject in which you can go for a PB:
        ",
        "nl":"
            Benoem een onderwerp waarop jij een PT wil behalen:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        body="""
        {"en":"
            My PB is a mark in:
        ",
        "nl":"
            Mijn PT is een cijfer voor
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            What higher mark are you aiming for?
        ",
        "nl":"
            Welk hoger cijfer mik je op?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            My PB is a better way of doing my university work or study in:
        ",
        "nl":"
            Mijn PT is het beter doen in mijn studie voor
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            The better way of doing things is:
        ",
        "nl":"
            De manier om dit te doen is:
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you believe you can reach this PB?
        ",
        "nl":"
            Denk je dat je deze PT kan behalen
        "}
        """,
        question_type="mc_yes_no" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            When do you plan to achieve this PB?
        ",
        "nl":"
            Wanneer wil je deze PT bereiken?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Describe the steps involved in reaching your PB and when they will be achieved
        ",
        "nl":"
            Beschrijf welke stappen je moet zetten om je PT te bereiken
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Did you reach your PB?
        ",
        "nl":"
            Heb jij je PT behaald?
        "}
        """,
        question_type="mc_learning_focus" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Provide evidence or a reason to support your answer to the previous question
        ",
        "nl":"
            Beschrijf en onderbouw je keuze voor de vorige vraag
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            My next PB is:
        ",
        "nl":"
            Mijn volgende PT is:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
learning_focus_comments_1 = [
    MockComment(
        body="""
        {"en":"
            Often when you focus on competing with others, you pay less attention to your own work. On the other hand, competition can be motivating to students. The good news is that there is a way to be competitive and also pay maximum attention to your own work. You do this by focusing on Personal Bests (PBs). A PB refers to the best you’ve ever done in something. Many elite swimmers and athletes will focus more on beating their PBs than beating others. In this exercise you will identify how you can achieve PBs.<br/><br/>(Do you remember your learning goal for Learning Focus? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            Als je focust op wedijveren met anderen besteed je minder aandacht aan je eigen werk. Aan de andere kant kan competitie een motivatie zijn voor studenten. Het goede nieuws is dat er een manier is om zowel competitief te zijn, maar ook maximale aandacht te besteden aan je eigen werk. Dit kan je doen door te focussen op Persoonlijke Topprestaties (PTs). Een PT refereert naar het beste wat je voor een bepaald gebied ooit hebt gedaan. Veel topatleten focussen meer op het verbeteren van hun eigen records dan het verslaan van anderen. In deze oefening leer je herkennen hoe jij jouw PTs kan bereiken.<br/><br/>(Heb je je leerdoel voor Learning Focus nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            You may choose to answer questions 2 & 3 or questions 4 & 5.
        ",
        "nl":"
            Beantwoord hieronder vraag 2 en 3, of vraag 4 en 5.
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            If you answered no, you need to develop a PB that you believe you can reach.
        ",
        "nl":"
            Bij NEE, omschrijf dan een PT die je wel kan behalen.
        "}
        """,
        location=6
    )
]

learning_focus_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {learning_focus_name} 1: Personal Bests (PBs)
        ",
        "nl":"
            {learning_focus_name} 1: Persoonlijke Topprestatie (PTs)
        "}}
        """,
    survey_type="action",
    construct_name=learning_focus_name,
    questions=learning_focus_questions_1,
    comments=learning_focus_comments_1
)

learning_focus_questions_2 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
learning_focus_comments_2 = [
  MockComment(
      body="""
        {"en":"
            (Do you remember your learning goal for Learning Focus? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Learning Focus nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
      location=0
  ),
  MockComment(
      body="""
        {"en":"
            A very  effective  way  of  understanding  and  remembering  your university work  is  to  be  an  active learner. You are an active learner when you act on what you learn. Examples are:<br/><ul><li>Summarizing a chapter in your own words</li><li>Writing notes in the margin of a chapter</li><li>Drawing a ‘mindmap’ (see next page)</li><li>Writing summary notes of a lesson</li></ul>
        ",
        "nl":"
            Een erg effectieve manier om je studiemateriaal te begrijpen en te onthouden, is om een actieve lerende te zijn. Dit ben je wanneer je handelt op wat je leert, bijvoorbeeld: <br/><ul><li>Een hoofdstuk samenvatting in je eigen woorden</li><li>Notities maken in de kantlijn van een hoofdstuk </li><li>Een ‘mindmap’ maken </li><li>Een korte samenvatting maken van een bepaald college</li></ul>
        "}
        """,
      location=0
  ),
  MockComment(
      body="""
        {"en":"
            In each of these examples you are acting on information.When you act on information it requires you to understand and think about it first. This makes you an active learner.
        ",
        "nl":"
            In elk van deze voorbeelden handel je op basis van informatie. Wanneer je handelt op basis van informatie, moet je die wel eerst begrijpen. Dat maakt je een actieve lerende.
        "}
        """,
      location=0
  ),
  MockComment(
      body="""
        {"en":"
            In this exercise you will work on a ‘mindmap’. A mindmap is a great way of drawing together a lot of information in one page.
        ",
        "nl":"
            In deze oefening ga je werken aan een ‘mindmap’. Dit is een goede manier om veel informatie met elkaar te verbinden op een pagina of overzicht.
        "}
        """,
      location=0
  ),
  MockComment(
      body="""
        {"en":"
            Select a  book  you  have  finished  reading  recently  (or  have  nearly finished)  and  fill  out  the  information requested in the mindmap over the page.
        ",
        "nl":"
            Kies een boek dat je recent hebt gelezen (of bijna uit hebt), en schrijf de benodigde informatie in de pagina waarop je mindmap komt.
        "}
        """,
      location=0
  ),
  MockComment(
      body="""
        {"en":"
            When you act on or transform information into your own words or your own mindmap then you are more likely to understand it and remember it. It can also be a good way of pulling together information for study notes leading up to an exam.
        ",
        "nl":"
            Wanneer je handelt op informatie of dit omzet in je eigen woorden of je eigen mindmap, is het waarschijnlijker dat je het begrijpt en onthoudt. Het kan ook een goede manier zijn om informatie uit verschillende bronnen samen te voegen in voorbereiden voor een tentamen.
        "}
        """,
      location=0
  ),
  MockComment(
      body="""
        {"en":"
            (Visual mindmap)
        ",
        "nl":"
            (Visuele mindmap)
        "}
        """,
      location=0
  ),
  MockComment(
      body="""
        {"en":"
            Middle mindmap: Write name of book you have finished recently or are reading now.<br/><ul><li>Describe the main theme/s in this book</li><li>What is this book about?</li><li>Who are the main characters?</li><li>Describe 2 of the main characters</li><li>Describe the style of writing. What do you think of the style?</li><li>Write out 1 strength of the book</li><li>Write out 1 weakness of the book</li><li>What was your favorite part of the book?</li><li>What do you think of the book overall?</li></ul>
        ",
        "nl":"
            Midden mindmap: Schrijf de naam van het boek dat je gelezen hebt of bijna uit hebt.<br/><ul><li>Beschrijf de belangrijkste thema’s in het book</li><li>Waar gaat het boek over? </li><li>Wie zijn de hoofdpersonen? </li><li>Beschrijf 2 hoofdpersonen </li><li>Beschrijf de schrijfstijl. Wat vind je hiervan?</li><li>Beschrijf 1 sterk punt van het boek </li><li>Beschrijf 1 zwak punt van het boek </li><li>Wat was je favoriete onderdeel van het boek? </li><li>Wat vind je over het algemeen van het boek? </li></ul>
        "}
        """,
      location=0
  ),
]

learning_focus_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {learning_focus_name} 2: Active Learning
        ",
        "nl":"
            {learning_focus_name} 2: Actief leren
        "}}
        """,
    survey_type="action",
    construct_name=learning_focus_name,
    questions=learning_focus_questions_2,
    comments=learning_focus_comments_2
)

learning_focus_questions_3 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Describe the last time you understood something that seemed difficult at first and why is this an achievement?
        ",
        "nl":"
            Wat was de laatste keer dat je iets moeilijks echt goed begreep, en waarom was dit een succes?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Describe the last time you you got really interested in something you were taught and why is this an achievement?
        ",
        "nl":"
            Wat was de laatste keer dat je echt geïnteresseerd was in iets dat je leerde, en waarom is dit een succes?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Describe the last time you learned something new and why is this an achievement?
        ",
        "nl":"
            Wat was de laatste keer dat je iets nieuws leerde, en waarom is di teen success?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Describe the last time you looked at an issue/situation in a new way and why is this an achievement?
        ",
        "nl":"
            Wat was de laatste keer dat je op een nieuwe manier naar een probleem of uitdaging hebt gekeken, en waarom was di teen success?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
learning_focus_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Learning Focus? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Learning Focus nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            To increase  your learning  focus it is also important  to  take  a  new look  at  achievement.  Although  marks and grades are a very important part of your achievements, there are usually other achievements on the way  to  getting  those  marks  or  grades. These  include  developing  skills,  solving  problems, and learning new things. Research shows that students who have a broader view of achievement that includes lots of different things (and not just  marks) enjoy university more and also do well. In this exercise you are asked to identify different types of achievements and why they are important. Complete the following questions.
        ",
        "nl":"
            Om je Learning focus te verhogen is het ook belangrijk om een nieuwe kijk op succes te ontwikkelen. Ook al zijn cijfers en studiepunten een heel belangrijk deel van je studiesucces, zijn er vaak ook andere successen te behalen om goede cijfers en studiepunten te krijgen. Dit zijn bijvoorbeeld het ontwikkelen van vaardigheden, het oplossen van problemen, en het leren van nieuwe dingen. Onderzoek wijst uit dat studenten met een bredere kijk op succes, waar veel verschillende dingen onder vallen, vaak meer plezier hebben in studeren en het ook beter doen. In deze oefening ga je verschillende soorten succes omschrijven, en waarom ze belangrijk zijn. Beantwoord de volgende vragen:
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            As you can see, there are different types of achievements at university –even before you receive your marks. From now on expand your idea of achievement to also include some of the things in the questions above
        ",
        "nl":"
            Zoals je kan zien zijn er verschillende types van succes bij het studeren aan een universiteit – zelfs voordat je je eerste cijfers krijgt. Verruim van nu af aan je idee over succes, en neem  ook een aantal van de aspecten hiervoor mee.
        "}
        """,
        location=4
    )
]

learning_focus_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {learning_focus_name} 3: A new look at achievement
        ",
        "nl":"
            {learning_focus_name} 3: Een nieuwe kijk op succes
        "}}
        """,
    survey_type="action",
    construct_name=learning_focus_name,
    questions=learning_focus_questions_3,
    comments=learning_focus_comments_3
)

learning_focus_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Learn to identify subjects in which you can achieve personal bests and how to do this</li><li>Learn to develop your ability for active learning</li><li>Learn to recognize many different types of achievement and why they are important</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leren om onderwerpen te vinden waar jij in kan excelleren en hoe je dit kan doen</li><li>Leren om vaardigheden te ontwikkelen voor actief leren</li><li>Leren om verschillende aspecten van succes te herkennen en waarom ze belangrijk zijn. </li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
learning_focus_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Learning focus is being focused on learning, solving problems, and developing skills. The goal of a learning focus is to be the best student you can be. If you are learning focused you tend to enjoy learning, do a good job for its own satisfaction and not just for rewards, and enjoy challenges.
        ",
        "nl":"
            Learning focus is de mate waarin je gefocust bent op leren, problemen oplossen en vaardigheden ontwikkelen. Het doel van een focus op leren is om de beste student te worden die je kan zijn. Het is ook je succesvol voelen en voldoening halen uit het beheersen van wat je wilde bereiken, of genieten van een goede uitdaging.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for developing a learning focus:<br/><ul><li>Focus more on doing your best and less on comparing yourself with other students in the class</li><li>Try to improve in your university work by competing with your own previous performance rather than competing with other students</li><li>See success as how much you improve and what progress you make rather than how many students you beat</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om een learning focus te ontwikkelen: <br/><ul><li>Focus meer op je best doen dan op het vergelijken met andere studenten.</li><li>Probeer te verbeteren in je studie door te vergelijken met je eigen prestaties in plaats van de competitie met anderen aangaan.</li><li>Zie succes als hoeveel jij verbeterd bent en welke voortuitgang je geboekt hebt, niet als hoeveel studenten je hebt verslagen.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for Learning focus. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Anxiety. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel:<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

learning_focus_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {learning_focus_name}
        ",
        "nl":"
            Voorbereiden: {learning_focus_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=learning_focus_name,
    questions=learning_focus_questions_prepare,
    comments=learning_focus_comments_prepare
)

learning_focus_questions_reflect = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Which of the last three Learning focus exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Learning Focus oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Identify subjects in which you can achieve personal bests and how to do this' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Herken onderwerpen waar jij je eigen leerdoelen kan behalen en hoe je dat kan doen’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Look for opportunities for active learning' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Zoek mogelijkheden om actief te leren’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Recognize many different types of achievement and why they are important' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Herken de verschillende soorten successen en waarom ze belangrijk zijn’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Learning Focus and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Learning Focus, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open"
    )
]
learning_focus_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Learning Focus Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst. <br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “I’ll make a special effort in Statistics to summarize text chapters in my own words”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Ik ga extra mijn best doen om hoofdstukken van statistiek in mijn eigen woorden samen te vatten”.)
        "}
        """,
        location=2
    )
]

learning_focus_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {learning_focus_name}
        ",
        "nl":"
            Reflecteren: {learning_focus_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=learning_focus_name,
    questions=learning_focus_questions_reflect,
    comments=learning_focus_comments_reflect
)

learning_focus = [learning_focus_1, learning_focus_2, learning_focus_3, learning_focus_prepare, learning_focus_reflect]
#endregion

#region valuing
valuing_questions_1 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Write down 3 university subjects, a world event or issue and how they are connected
        ",
        "nl":"
            Beschrijf 3 studieonderdelen, een gebeurtenis in de wereld, en hoe ze verbonden zijn.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
valuing_comments_1 = [
    MockComment(
        body="""
        {"en":"
            You value university more when you can see the connections between what you learn and events in the world or hot issues/debates. There are many parts of university and university subjects that can teach you a lot about the world. In this exercise you will look for links between some university subjects and world events.
        ",
        "nl":"
            De waarde die je toekent aan studeren aan een universiteit kan vergroten wanneer je een verbinding ziet met wat je leert en gebeurtenissen in de wereld. Er zijn verschillende onderdelen van studeren die je wat kunnen leren over de wereld en de maatschappij. In deze oefening ga je zoeken naar hoe je studie verbonden is met gebeurtenissen in de wereld.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <ul><li>Write the names of 3 university subjects in the question below.</li><li>Read through a major daily newspaper (no more than a week old).</li><li>Identify events or issues that are connected to each subject.</li><li>Describe how they are connected.</li></ul>
        ",
        "nl":"
            <ul><li>Schrijf hieronder 3 studieonderdelen.</li><li>Lees (online) een belangrijk nieuwsblad of krant (niet ouder dan een week)</li><li>Beschrijf welke gebeurtenissen verbonden zijn aan een studieonderdeel</li><li>Beschrijf hoe ze verbonden zijn</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            These are just a few ways in which what you learn is hooked into the world and show that when you look closely, university is relevant to the world in lots of ways. As much as possible take notice of what you read, hear, and see in the news and think about how this is connected to what you learn at university.
        ",
        "nl":"
            Dit zijn maar een paar manieren waarop je kan leren hoe je studie en wereldgebeurtenissen met elkaar te maken hebben. Als je goed kijkt, zie je dat je studie op meerdere manieren verbonden kan zijn. Probeer wat je leest, ziet en hoort in het nieuws te linken aan je studie.
        "}
        """,
        location=1
    )
]

valuing_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {valuing_name} 1: Hooking university into the world
        ",
        "nl":"
            {valuing_name} 1: Studie verbinden met de wereld
        "}}
        """,
    survey_type="action",
    construct_name=valuing_name,
    questions=valuing_questions_1,
    comments=valuing_comments_1
)

valuing_questions_2 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Write down 3 university subjects, an aspect of your life and how the two are connected
        ",
        "nl":"
            Beschrijf 3 studieonderdelen, een aspect van jouw leven, en hoe die twee verbonden zijn.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
valuing_comments_2 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for valuing? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Valuing control nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            You value university more when you can see the connections between what you learn at university and your own  life. You may be surprised when you take a look at the  different ways you can actually use things you learn at university in other parts of your life. In this exercise you will look for links between some university subjects and aspects of your own life.
        ",
        "nl":"
            De waarde die je toekent aan studeren aan een universiteit kan vergroten als je de connective ziet met je eigen leven. Het kan je verbazen op hoeveel manieren je kan toepassen wat je leert in je studie in je dagelijkse leven. In deze oefening ga je kijken naar de verbinding tussen studieonderdelen en aspecten van je eigen leven.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <ul><li>Write the names of 3 subjects in the question below.</li><li>Identify an aspect, experience, problem, or issue in your own life that is somehow connected to one of the subjects.</li><li>Describe how it is connected.</li></ul>
        ",
        "nl":"
            <ul><li>Beschrijf hieronder 3 studieonderdelen</li><li>Beschrijf een aspect, ervaring, of probleem in jouw leven dat een connective heeft met een onderdeel </li><li>Beschrijf hoe het verbonden is.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            These are just a few ways in which what you learn is hooked into your own life and show that when you look closely, university is relevant to your life in a number of ways
        ",
        "nl":"
            Dit zijn maar een paar manieren hoe je kan kijken naar de verbinding tussen je studie en je dagelijks leven. Als je goed kijk, zul je zien dat ze op verschillende manieren verbonden zijn.
        "}
        """,
        location=1
    )
]

valuing_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {valuing_name} 2: Hooking university into my life
        ",
        "nl":"
            {valuing_name} 2: Studie verbinden met mijn leven
        "}}
        """,
    survey_type="action",
    construct_name=valuing_name,
    questions=valuing_questions_2,
    comments=valuing_comments_2
)

valuing_questions_3 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Write down 3 university subjects, for each subject a skill that you developed in it and an aspect of your life in which it may be useful for
        ",
        "nl":"
            Beschrijf 3 studieonderdelen, voor elk onderdeel welke vaardigheid je daar hebt ontwikkeld, en hoe je die kan toepassen in andere onderdelen van je leven.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
valuing_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for valuing? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Valuing control nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            You also value university more when you can see that you learn skills at university that can help you in different  parts of your life. Skills you learn include: how to  communicate, how to solve problems, how to justify your arguments and ideas, how to solve problems, how to resolve conflict, how to negotiate, how to plan, how to organize your time, and how to analyze. In this exercise you will look at skills you learn in some subjects and how you can use them in other parts of your life.
        ",
        "nl":"
            De waarde die je toekent aan studeren aan een universiteit kan ook vergroten wanneer je ziet dat je daar nieuwe vaardigheden hebt ontwikkeld die je in andere delen van je leven kan toepassen. Dit zijn vaardigheden als: hoe te communiceren, hoe je problemen kan oplossen, hoe je ideën kan beargumenteren, hoe je conflicten kan oplossen, hoe je kan onderhandelen, hoe je kan plannen, en hoe je kan analyseren. In deze oefening ga je kijken naar vaardigheden die je geleerd hebt in je studie en hoe je die kan toepassen in andere delen van je leven.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <ul><li>Write the names of 3 subjects in the table below.</li><li>Identify a key skill you have developed in this subject</li><li>Identify an aspect of your life (eg. personal, social, work) that this skill is or could be particularly useful</li></ul>
        ",
        "nl":"
            <ul><li>Beschrijf hieronder 3 studieonderdelen </li><li>Beschrijf een cruciale vaardigheid die je daar hebt ontwikkeld</li><li>Beschrijf een aspect van je leven (bijv. Persoonlijk, social, op je werk) waar je die vaardigheid kan toepassen of waar die nuttig is.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            As you can see, there are a number of important skills you develop at university that can be useful in other parts of your life
        ",
        "nl":"
            Zoals je kan zien zijn er verschillende belangrijke vaardigheden die je hebt ontwikkeld op de universiteit, die ook nuttig zijn in andere delen van je leven.
        "}
        """,
        location=1
    )
]

valuing_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {valuing_name} 3: Skills I learn at university
        ",
        "nl":"
            {valuing_name} 3: Vaardigheden geleerd in mijn studie
        "}}
        """,
    survey_type="action",
    construct_name=valuing_name,
    questions=valuing_questions_3,
    comments=valuing_comments_3
)

valuing_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Make connections between what you learn at university and world events and hot issues</li><li>Make connections between what you learn at university and your own life</li><li>Identify skills you learn at university and how these skills help you in other parts of your life</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Maak connecties tussen wat je leert tijdens je studie en gebeurtenissen in de wereld. </li><li>Maak connecties tussen wat je leert tijdens je studie en je eigen leven.</li><li>Identificeer de vaardigheden die je leert tijdens je studie, en hoe deze je op andere momenten of later in je leven kunnen helpen.</li></ol>
        """,
        question_type="open",
        required=False
    ),
]
valuing_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Valuing university is how much you believe what you learn at university is useful, important, and relevant to you or to the world in general. If you value university you tend to be interested in what you learn, persist when university work gets difficult, and enjoy university.
        ",
        "nl":"
            Valuing is de mate waarin jij gelooft dat wat je leert op de universiteit nuttig, belangrijk, en relevant is voor jou of de wereld in het algemeen. Als je waarde hecht aan studeren aan een universiteit, ben je waarschijnlijk meer geïnteresseerd in wat je leert, heb je meer doorzettingsvermogen wanneer het moeilijk wordt, en is studeren leuker.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for developing a valuing of university:<br/><ul><li>Look for links between what you learn at university and world events or hot issues</li><li>Look for links between what you learn at university and how it can be used in other parts of your life</li><li>Look for links between what you learn at university and your interests</li><li>Think about what you learn at university and how it could be useful for what you might do after you leave university</li><li>Understand that you learn more than just facts at university. You also learn how to think and to analyze and this will help you in many parts of your life such as solving problems, making major decisions, dealing with personal issues, and work</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om je Valuing te ontwikkelen: <br/><ul><li>Kijk naar connecties tussen wat je leert tijdens je studie en gebeurtenissen in de wereld om je heen.</li><li>Kijk naar connecties tussen wat je leert tijdens je studie, en hoe je dat kan inzetten op andere delen van je leven</li><li>Kijk naar connecties tussen wat je leert tijdens je studie, en hoe dat aansluit bij je eigen interesses</li><li>Denk na over wat je leert tijdens je studie, en hoe dat nuttig kan zijn wanneer je klaar bent met studeren.</li><li>Probeer te begrijpen dat je meer leert dan alleen feitjes wanneer je studeert. Je leert bijvoorbeeld ook analytisch te denken, dat kan je helpen op andere vlakken in je leven, wanneer je keuzes moet maken, of wanneer je problemen moet oplossen.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for valuing. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Valuing. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel:<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

valuing_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {valuing_name}
        ",
        "nl":"
            Voorbereiden: {valuing_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=valuing_name,
    questions=valuing_questions_prepare,
    comments=valuing_comments_prepare
)

valuing_questions_reflect = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Which of the last three Valuing exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Valuing oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Make connections between what you learn at university and world events' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Leg verbanden tussen wat je leert op de universiteit en gebeurtenissen in de wereld’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Make connections between what you learn at university and your own life' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Leg verbanden tussen wat je leert op de universiteit en je eigen leven’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Identify skills you learn at university and how they help you in other parts of your life' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Herken vaardigheden die je leert tijdens je studie en hoe je die kan toepassen in andere delen van je leven’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Valuing and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Valuing, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open"
    )
]
valuing_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Valuing Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “Learning how to look at evidence and facts helps me to make better decisions”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Leren hoe bewijs en feiten me kunnen helpen om betere beslissingen te maken”)
        "}
        """,
        location=2
    )
]

valuing_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {valuing_name}
        ",
        "nl":"
            Reflecteren: {valuing_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=valuing_name,
    questions=valuing_questions_reflect,
    comments=valuing_comments_reflect
)

valuing = [valuing_1, valuing_2, valuing_3, valuing_prepare, valuing_reflect]
#endregion

#region persistence
persistence_questions_1 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Write down below the 30-minute blocks consisting of what you need to do (e.g. make a rough essay plan), followed by when you start (e.g. 6:00) and when you finish (e.g. 6:28), and finally what you will do after you finish (e.g. take a 2 minute break)
        ",
        "nl":"
            Beschrijf hieronder de blokken van 30 minuten, inclusief wat je moet doen (bijv. een concept maken van je paper), gevolgd door wanneer je start (bijv. 18:00), wanneer je klaar bent (bijv. 18:30), en wat je daarna doet (bijv. een pauze van 2 minuten).
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
persistence_comments_1 = [
    MockComment(
        body="""
        {"en":"
            Students often give up on study, assignments, or projects when the mountain seems too big to climb. For example, tackling a 2-hour study session may seem overwhelming. The 30 x 2 plan can help here. Here you (a) chunk your night’s study into 30-minute blocks, (b) tick off every 30-minutes completed, (c) build in a 2-minute break at the end of the first 30 minutes, and (d) build in a 5-minute break at the end of the second 30 minutes. When you do this, the study session becomes more manageable. Even better, the time seems to go faster! Right now you will plan tonight’s study using the 30 x 2 plan. Follow this plan tonight.
        ",
        "nl":"
            Studenten geven vaak op in hun studie, bij studieopdrachten, of projecten wanneer de uitdaging te groot lijkt. Het tackelen van een 2-uur durende studiesessie kan best overweldigend zijn. Het 30 x 2 plan kan hierbij helpen. Hierin a) deel je je studieschema op in blokken van 30 minuten, b) vink je elke 30 minuten af, c) plan je een pauze van 2 minuten aan het einde van de eerste 30 minuten, en d) plan je een pauze van 5 minuten na de tweede 30 minuten. Als je dit doet worden de studiesessies beter vol te houden. Sterker nog, de tijd lijkt soms zelfs sneller te gaan. Nu ga je je eerste studiesessie plannen met het 30 x 2 plan.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            This is one way to ‘chunk’ larger tasks into smaller ones. It has helped many students get through assignments and study sessions that seemed overwhelming at first.
        ",
        "nl":"
            Dit is een manier om grote taken of studiesessies op te delen in behapbare delen. Dit heeft al veel studenten geholpen om door opdrachten en studiesessies heen te komen die in eerste instantie overweldigend leken.
        "}
        """,
        location=1
    )
]

persistence_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {persistence_name} 1: The 30 X 2 plan
        ",
        "nl":"
            {persistence_name} 1: Het 30 x 2 plan
        "}}
        """,
    survey_type="action",
    construct_name=persistence_name,
    questions=persistence_questions_1,
    comments=persistence_comments_1
)

persistence_questions_2 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Describe the last difficult university work task that you persisted at and broke through to complete <i>(eg. “I found my last Science report really difficult, but I got there in the end”)</i>
        ",
        "nl":"
            Beschrijf de laatste moeilijke studieopdracht waar je doorgezet hebt om het te bereiken <i>(bijv. “De laatste opdracht voor statistiek vond ik heel moeilijk, maar uiteindelijk is het me gelukt”)</i>
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            What sorts  of  things  did  you <b>THINK</b> or say  to  yourself  that helped  you  get  through  when  things  started getting difficult? <i>(eg.“I’ve done similar tasks before” or “I’ll take it one step at a time” or “I’ll get as far as I can and then check out the Internet”)</i>
        ",
        "nl":"
            Welke dingen <b>denk</b> of zeg je tegen jezelf die helpen doorzetten wanneer het moeilijk wordt? <i>(bijv. “ik heb in het verleden al zulke opdrachten kunnen maken” of “Ik doe het stap voor stap”, of “Ik ga proberen zo ver mogelijk te komen en anders zoek ik online”)</i>
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            What sorts of things did you <b>DO</b> that helped you get through when things started getting difficult? <i>(eg. “I asked for help” or “I checked out the Internet” or “I worked at things I knew first to build my confidence”)</i>
        ",
        "nl":"
            Welke dingen <b>deed</b> je die hielpen om door de moeilijke opdracht heen te komen? <i>(bijv. “Ik vroeg om hulp” of “ik zocht online naar oplossingen” of “ik deed eerst de dingen die ik wist voor mijn zelfvertrouwen”)</i>
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            What have you learnt from this that can be used to help you on the next difficult university work task? <i>(eg. “Working through difficult tasks gives me confidence for next time”)</i>
        ",
        "nl":"
            Wat heb je hiervan geleerd dat nuttig kan zijn bij een volgende uitdagende studieopdracht? <i>(Bijv. “Doorzetten bij een moeilijke studieopdracht geeft me zelfvertrouwen voor de volgende keer”)</i>
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
persistence_comments_2 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Persistence? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Persistence nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begin.)
        "}
        """,
        location=0
    ),
    MockComment(
      body="""
        {"en":"
            Students often  forget  that  they  have  persisted  at  difficult university work  in  the  past.  Students usually persist in subjects that they like or are confident in. But the same principles apply for subjects that they may not enjoy so much or thatthey are not so confident in.
        ",
        "nl":"
            Studenten vergeten vaak dat ze al vaker door moeilijk studiewerk heen zijn gekomen. Dit vinden ze vaak gemakkelijker bij vakken of onderdelen die ze leuk vinden of meer zelfvertrouwen in hebben. Maar dezelfde principes gelden voor onderdelen waar je minder plezier aan beleeft of waar ze minder zelfvertrouwen in hebben.
        "}
        """,
      location=0
    ),
    MockComment(
        body="""
        {"en":"
            In this exercises you will identify a time when you persisted at difficult university work and broke through to complete it.
        ",
        "nl":"
            In deze oefening benoem je een keer dat jij doorgezet hebt in een moeilijke studieopdracht en deze succesvol hebt afgerond.
        "}
        """,
        location=0
    )
]

persistence_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {persistence_name} 2: When I broke through last time
        ",
        "nl":"
            {persistence_name} 2: Toen ik er de vorige keer doorheen kwam
        "}}
        """,
    survey_type="action",
    construct_name=persistence_name,
    questions=persistence_questions_2,
    comments=persistence_comments_2
)

persistence_questions_3 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In what subject do you tend to give up a bit too easily?
        ",
        "nl":"
            Bij welk onderwerp geef je misschien iets te makkelijk op?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Who can you ask for help in this subject? (select people whose knowledge can be relied upon)
        ",
        "nl":"
            Wie kan je om hulp vragen bij dit onderwerp (Who can you ask for help in this subject? (kies personen op wiens kennis je kan vertrouwen)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Who is a good study buddy you can use in this subject? (pick a study buddy –not a social distraction)
        ",
        "nl":"
            Wie is een goed studiemaatje en kan je helpen in dit onderwerp (kies een studiemaatje – geen sociale afleiding)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            What other sources can you draw on? (eg. previous similar questions or examples, Internet, other books etc.)
        ",
        "nl":"
            Welke andere bronnen kan je gebruiken? (bijv. vergelijkbare opdrachten of voorbeelden, internet, boeken, etc.)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            What have you learnt from this that can be used to help you on the next difficult task? <i>(eg. “If I get as far as I can, I’ll then look through the textbook for similar problems and what hints this can give me”)</i>
        ",
        "nl":"
            Wat heb je hiervan geleerd dat nuttig kan zijn voor de volgende moeilijke opdracht? (Bijv. “Ik ga proberen zo ver te komen als ik kan, dan zoek ik in een boek of een andere plek voor hints en tips)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    ),
]
persistence_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Persistence? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Persistence nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Students often give up on difficult tasks because they don’t have a back-up plan or strategies to use when they ‘hit the wall’
        ",
        "nl":"
            Studenten geven vaak op bij een moeilijke opdracht omdat ze geen back-up plan of strategie hebben wanneer ze ‘tegen de muur lopen’.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In this exercise you will explore some strategies that may be useful at these times
        ",
        "nl":"
            In deze oefening ga je een aantal strategieen verkennen die nuttig kunnen zijn bij zulke momenten.
        "}
        """,
        location=0
    ),
]

persistence_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {persistence_name} 3: When I hit the wall
        ",
        "nl":"
            {persistence_name} 3: Als ik tegen een muur loop
        "}}
        """,
    survey_type="action",
    construct_name=persistence_name,
    questions=persistence_questions_3,
    comments=persistence_comments_3
)

persistence_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Learn to identify subjects in which you can achieve personal bests and how to do this</li><li>Learn to develop your ability for active learning</li><li>Learn to recognize many different types of achievement and why they are important</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leer hoe je lange studiesessies kan opdelen in behapbare delen.</li><li>Leer te herkennen hoe je eerdere uitdagingen en moeilijkheden hebt overwonnen.</li><li>Leer hoe je in de toekomst uitdagingen en moeilijkheden in je studie kan overwinnen.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
persistence_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Persistence is how much you keep trying to work out an answer or to understand a problem even when that problem is difficult or is challenging. If you are persistent you tend to achieve what you set out to do, are more motivated to succeed, and are good at problem solving
        ",
        "nl":"
            Persistence (Doorzettingsvermogen) is hoe lang en hard je blijft proberen om een antwoord te formuleren of een probleem te begrijpen, zelfs als dat moeilijk of uitdagend is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for developing a persistence:<br/><ul><li>Be clear as to what you want to achieve in an assignment or an exam and why you want to achieve it. This is called goal-setting. Goal-setting increases your persistence</li><li>Think carefully about what it is you will need to do to achieve your goal. This involves breaking tasks into smaller parts (chunking). For example, for an assignment you may want to think about the books you can read, where you can get more information, and how you can present your work</li><li>Remember to set goals that are:<ul><li>Achievable (they should match your age and ability)</li><li>Believable (you must believe that you can reach them)</li><li>Clear (you must be able to clearly say what they are)</li><li>Desirable (you must choose goals that you want to reach)</li></ul></li><li>Think carefully about what difficulties you may have in achieving your goal and how you can overcome those difficulties. For example, there may not be many books in your library about your assignment topic so you will need to go to another library and also surf the Internet</li><li>Think about times before that you’ve overcome challenge or obstacles to success and what you did or thought that helped you overcome them</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> om je Persistence (doorzettingsvermogen) te ontwikkelen:<br/><ul><li>Wees duidelijk over wat je wil bereiken bij een opdracht of een examen, en waarom je dat wil bereieken. Dit heet ‘goal-setting’, dat verhoogt je doorzettingsvermogen.</li><li>Denk goed na over wat je moet doen om je doel te bereiken. Hierbij kan je opdrachten of taken in kleinere stukjes opdelen (‘chunking’). Je kan bijvoorbeeld voor een opdracht nadenken over welke boeken of artikelen je wil lezen, waar je extra informatie kan vinden, of hoe je je opdracht het best kan presenteren.</li><li>Onhoud dat je doelen stelt die:<ul><li><i>Achievable</i> of haalbaar zijn (dus die passen bij jouw leeftijd en capaciteiten).</li><li><i>Believable</i> of geloofwaardig zijn (jij moet erin geloven dat je die doelen kan behalen).</li><li><i>Clear</i> of helder geformuleerd zijn (je moet ze helder uiteen kunnen zetten).</li><li><i>Desirable</i> of wenselijk zijn (jij moet doelen stellen die jij wenselijk vindt).</li></ul></li><li>Bedenk goed welke moeilijkheden of uitdagingen je tegen kan komen wanneer je je doelen wil bereiken en hoe je die kan overwinnen. Het kan bijvoorbeeld zo zijn dat er weinig boeken in de bibliotheek zijn over jouw specifieke onderwerp dus zul je op zoek moeten gaan naar andere manieren om informatie te verzamelen.</li><li>Denk terug aan keren waar je een uitdaging of moeilijkheid overwonnen hebt, en hoe je dit precies hebt gedaan.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for Persistence. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Persistence. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel:<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

persistence_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {persistence_name}
        ",
        "nl":"
            Voorbereiden: {persistence_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=persistence_name,
    questions=persistence_questions_prepare,
    comments=persistence_comments_prepare
)

persistence_questions_reflect = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Which of the last three Persistence exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Persistence oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Break longer study sessions into smaller parts' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Deel lange studiesessie op in kleinere delen’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Identify times you overcame challenges in the past and how you did this.' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Herken de keren wanneer je uitdagingen overwonnen hebt, en hoe je dit hebt gedaan.’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Identify ways you can overcome challenges in university subjects in the future' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Herken manieren waarmee je in de toekomst uitdagingen kan overwinnen in je studie’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen
        "}
        """,
        question_type="likert_7" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Persistence and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Persistence, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open"
    )
]
persistence_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Persistence Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “On difficult university work, I’ll think about ways I’ve got through tough work before)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Voor moeilijke studieopdrachten bedenk ik hoe ik eerder door zulke opdrachten heen ben gekomen”)
        "}
        """,
        location=2
    )
]

persistence_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {persistence_name}
        ",
        "nl":"
            Reflecteren: {persistence_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=persistence_name,
    questions=persistence_questions_reflect,
    comments=persistence_comments_reflect
)

persistence = [persistence_1, persistence_2, persistence_3, persistence_prepare, persistence_reflect]
#endregion

#region planning
planning_questions_1 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Understand the question/task
        ",
        "nl":"
            Goed begrijpen wat de vraag of taak is
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Break question into parts
        ",
        "nl":"
            Vragen opdelen in kleinere delen
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Initial search for information (eg. internet, library, etc)
        ",
        "nl":"
            Eerste zoekopdracht voor informatie (bijv. Op internet, in de bibliotheek, etc.) 
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Focused and detailed reading of books and other resources collected
        ",
        "nl":"
            Gefocussed en op de details lezen van boeken of andere verzamelde materialen
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Detailed summary of information
        ",
        "nl":"
            Een gedetailleerde samenvatting van de informatie maken
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Organize information (eg. put information under each heading)
        ",
        "nl":"
            Informatie organisren (bijv. Informatie opdelen onder kopjes)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Write first draft
        ",
        "nl":"
            Eerste concept schrijven
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Tie up loose ends (eg. a bit more reading)
        ",
        "nl":"
            Losse eindjes aan elkaar knopen (bijv. Iets meer lezen)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Write second draft
        ",
        "nl":"
            Tweede concept schrijven
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Edit (eg. spelling, grammar, formatting checks)
        ",
        "nl":"
            Wijzigingen maken (bijv. spelling, grammatica, opmaak)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Final draft
        ",
        "nl":"
            Definitieve versie maken
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Reward yourself for completing the assignment
        ",
        "nl":"
            Jezelf belonen voor het afronden van de opdracht
        "}
        """,
        question_type="open"
    )
]
planning_comments_1 = [
    MockComment(
        body="""
        {"en":"
            In this exercise you will identify the steps involved in doing an assignment or project and how to do each part. Knowing all the different parts that go together to do an assignment or study is very important. The questions below are the key steps in doing an assignment or project. At each step you need to allocate your time and briefly describe how you will do it.
        ",
        "nl":"
            In deze oefening ga je de stappen identificeren die nodig zijn om een opdracht of project uit te voeren, en hoe je die stappen kan uitvoeren. Weten wat de verschillende delen zijn van een opdracht of van je studie is erg belangrijk. De vragen hieronder zijn de sleutel om opdrachten of projecten uit te voeren. Bij elke stap bepaal je hoeveel tijd het gaat kosten, en hoe je het gaat doen.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            As you can see, there are many steps to completing an assignment or project. When you get it clear in your mind what you need to do for each part you are more likely to stay on track and do better.
        ",
        "nl":"
            Zoals je kan zien zijn er verschillende stappen nodig om een opdracht of project af te ronden. Wanneer je voor jezelf duidelijk hebt wat je moet doen voor elke stap, lukt het waarschijnlijk beter.
        "}
        """,
        location=12
    )
]

planning_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {planning_name} 1: Planning what to do and how to do it
        ",
        "nl":"
            {planning_name} 1: Plannen, wat en hoe
        "}}
        """,
    survey_type="action",
    construct_name=planning_name,
    questions=planning_questions_1,
    comments=planning_comments_1
)

planning_questions_2 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Analyze
        ",
        "nl":"
            Analyzeren
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Compare
        ",
        "nl":"
            Vergelijken
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Contrast
        ",
        "nl":"
            Contrasteren
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Define
        ",
        "nl":"
            Definiëren
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Describe
        ",
        "nl":"
            Beschrijven
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Discuss
        ",
        "nl":"
            Bediscussieer
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Evaluate
        ",
        "nl":"
            Evalueer
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Justify
        ",
        "nl":"
            Verantwoord
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Summarize
        ",
        "nl":"
            Samenvatten
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    ),
]
planning_comments_2 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Planning? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Planning nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            To develop a good plan for an assignment or study and to know you’re on-track,  it is  important  to  fully understand  what  you’re  being  asked  to  do.  Often  students  do  not  spend  enough  time  analyzing  the question and understanding each part of it. Because of this they do not answer the question properly. In this exercise you will describe in your own words some key words that are often used in assignmentand exam  questions.  In  the  table  below  are  some  of  these  key  words  commonly  used  in  exam  and assignment questions. For each word, describe what it means – <b>use a dictionary or ask a lecturer/tutorand then put it in your own words</b>
        ",
        "nl":"
            Om een goede planning voor een opdracht of voor je studie te maken, en om te weten of je nog op de juiste weg bent, is het belangrijk om goed te begrijpen wat er van je gevraagd wordt. Studenten besteden vaak niet genoeg tijd aan het proberen te begrijpen van de vraag en uit welke onderdelen deze bestaat. Hierdoor geven ze dan ook geen goed antwoord op de vraag. In deze oefening beschrijf je een aantal sleutelwoorden die in tentaments gebruikt worden in je eigen woorden. Hieronder vind je een aantal sleutelwoorden die regelmatig gebruikt worden in tentamens. Schrijf voor elk woord eerst op wat het betekent <b>met behulp van een woordenboek of een docent, en vervolgens in je eigen woorden.</b>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            These definitions will ensure that you better understand many exam and assignment questions in the future
        ",
        "nl":"
            Met deze definities begrijp je in de toekomst tentamenvragen en opdrachten waarschijnlijk beter, zodat je ook beter antwoord kan geven.
        "}
        """,
        location=9
    )
]

planning_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {planning_name} 2: Understand what I'm being asked to do
        ",
        "nl":"
            {planning_name} 2: Begrijpen wat mij gevraagd wordt
        "}}
        """,
    survey_type="action",
    construct_name=planning_name,
    questions=planning_questions_2,
    comments=planning_comments_2
)

planning_questions_3 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In what subjects do you need to re-read my answer/essay when I have finished writing
        ",
        "nl":"
            Voor welk onderdeel van je studie kan ik mijn antwoord of paper herlezen wanneer ik denk dat ik klaar ben
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In what subjects do you need to double-check my calculations
        ",
        "nl":"
            Voor welk onderdeel van je studie kan ik mijn berekeningen controleren
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In what subjects do you need to spend more time reading the question
        ",
        "nl":"
            Voor welk onderdeel van je studie kan ik meer tijd besteden bij het lezen van de vraag
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In what subjects do you need to check a dictionary or thesaurus if I don’t understand a word
        ",
        "nl":"
            Voor welk onderdeel van je studie kan ik een woordenboek gebruiken als ik een term niet begrijpt
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In what subjects do you need to check that each part of the question has been answered
        ",
        "nl":"
            Voor welk onderdeel van je studie kan ik checken of elk onderdeel van de vraag beantwoord is
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            In what subjects do you need to pause a moment to think before I write the first thing that comes to mind
        ",
        "nl":"
            Voor welk onderdeel van je studie kan ik een korte denkpauze nemen voordat je begint met schrijven
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Can you think of more strategies and in what subjects you need to do apply them to?
        ",
        "nl":"
            Kan je nog meer strategieën bedenken en studieonderdelen waar je ze kan toepassen?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
planning_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Planning? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Planning nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Checking that you are answering the question is important for success on exams and assignments. In this exercise you will look at strategies you can use to check your work in different university subjects.
        ",
        "nl":"
            Checken of je vragen echt beantwoord is belangrijk voor het halen van een tentamen of opdracht. In deze oefening kijk je naar strategieën die je kan gebruiken om je werk te controleren bij verschillende onderdelen van je studie.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the questions below, write out the subjects that could benefit from each checking strategy
        ",
        "nl":"
            Beschrijf per vraag hieronder voor welk onderdeel van je studie dit nuttig kan zijn
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Make a copy of these tables and pin it on your wall at home and in your diary or term planner. Checking you are on-track will improve your university work and results.
        ",
        "nl":"
            Kopieer deze antwoorden, hang ze thuis op, of zet ze in je agenda of planner. Regelmatig monitoren of je nog op de juiste koerst bent helpt bij het halen van betere resultaten.
        "}
        """,
        location=7
    )
]

planning_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {planning_name} 3: Checking I'm on track
        ",
        "nl":"
            {planning_name} 3: Check je koers
        "}}
        """,
    survey_type="action",
    construct_name=planning_name,
    questions=planning_questions_3,
    comments=planning_comments_3
)

planning_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol></li>Learn how to break your university work into parts</li></li>Learn to understand key words often used in exams and assignments</li></li>Learn to develop strategies to help you keep on track when doing assignments and exams</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leer hoe je je opdrachten in kleinere delen kan opdelen.</li><li>Leer sleutelwoorden begrijpen die vaak gebruikt worden in examens en opdrachten.</li><li>Leer strategieën te ontwikkelen die je helpen op het juiste spoor te blijven wanneer je een examen of een opdracht maakt.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
planning_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Planning is how much you plan your assignments and study and how much you keep track of your progress as you are doing them. If you plan your university work you tend to feel in control of your university work, persist at challenging university work, and make good use of your time and your abilities.
        ",
        "nl":"
            Planning is hoeveel je het studeren en maken van opdrachten plant. Het gaat ook over het bijhouden van voortgang wanneer je opdrachten maakt of studeert. Als je studieonderdelen goed plant, is het waarschijnlijker dat je controle voelt over je studie, meer doorzettingsvermogen hebt, en je tijd en capaciteit optimaal benut.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for planning:<br/><ul><li>Break assignments into parts, outline what you need to do for each part, and carefully think about how to do each part</li><li>Understand what you have been asked to do in exams and assignments. For example, be very clear on what key words (eg. compare and contrast, analyze, discuss, justify etc.) mean</li><li>Frequently return to the essay or test question as you are answering it to make sure you are on track, double check your answers, read questions carefully, re-read your answers</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> voor planning:<br/><ul><li>Verdeel opdrachten in kleinere delen, bedenk wat je voor elk deel moet doet, en denk goed na over hoe je dat gaat doen.</li><li>Probeer te begrijpen wat je precies moet doen in een examen of voor een opdracht. Let bijvoorbeeld goed op sleutelwoorden zoals ‘vergelijk’, ‘analyseer’, ‘discussieer’, ‘verantwoord’, etc.</li><li>Kijk meerdere malen naar de opdrachtbeschrijving of de examenvraag wanneer je daaraan werkt. Zo weet je of je nog op het goede spoor zit, kan je je antwoorden dubbel checken, kan je de vraag nogmaals goed lezen en je antwoord daaraan koppelen.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for Planning. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Planning. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel:<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

planning_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {planning_name}
        ",
        "nl":"
            Voorbereiden: {planning_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=planning_name,
    questions=planning_questions_prepare,
    comments=planning_comments_prepare
)

planning_questions_reflect = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Which of the last three Planning exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Planning oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Learn how to break your university work into parts' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Leren hoe je studieopdrachten in kleine delen kan opdelen’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Get to understand key words often used in exams and assignments' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Sleutelwoorden leren begrijpen die vaak worden gebruikt in opdrachten en examens’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Develop strategies to help you keep on track when doing assignments and exams' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Strategieën ontwikkelen die je helpen wanneer je een opdracht of examen maakt’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Planning and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Planning, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open"
    )
]
planning_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Planning Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “I’ll make a special effort in Statistics to summarize text chapters in my own words”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Ik ga mijn opdrachten in behapbare stukjes opdelen en ze afvinken wanneer ik ermee klaar ben”)
        "}
        """,
        location=2
    )
]

planning_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {planning_name}
        ",
        "nl":"
            Reflecteren: {planning_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=planning_name,
    questions=planning_questions_reflect,
    comments=planning_comments_reflect
)

planning = [planning_1, planning_2, planning_3, planning_prepare, planning_reflect]
#endregion

#region task_management
task_management_questions_1 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well at home, if so in which room?
        ",
        "nl":"
            Studeer je thuis goed, en zo ja in welke kamer?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well at the library, if so which library?
        ",
        "nl":"
            Studeer je in de bibliotheek goed, en zo ja waar in de bibliotheek?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well somehwere else, if so where?
        ",
        "nl":"
            Studeer je ergens anders goed, en zo ja, waar?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well on weekdays, if so which days?
        ",
        "nl":"
            Studeer je goed op werkdagen, en zo ja op welke?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well during the weekend, if so which days?
        ",
        "nl":"
            Studeer je goed in het weekend, en zo ja welke dag?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well in the morning, if so at what time?
        ",
        "nl":"
            Studeer je goed in de ochtend, en zo ja hoe laat?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well in the afternoon, if so at what time?
        ",
        "nl":"
            Studeer je goed in de middag, en zo ja hoe laat?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well at night, if so at what time?
        ",
        "nl":"
            Studeer je goed in de avond, en zo ja hoe laat?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well alone?
        ",
        "nl":"
            Studeer je goed in je eentje?
        "}
        """,
        question_type="mc_yes_no" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well with a friend, if so what friend (select carefully)?
        ",
        "nl":"
            Studeer je goed met een vriend, en zo ja met wie (wees kieskeurig)?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well in a group, if so who are they (select carefully)?
        ",
        "nl":"
            Studeer je goed in een groep, en zo ja met wie? (wees kieskeurig)
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well in a quiet room without distractions?
        ",
        "nl":"
            Studeer je goed in een rustige kamer zonder afleidingen?
        "}
        """,
        question_type="mc_yes_no" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well with background activity (eg. radio)?
        ",
        "nl":"
            Studeer je goed met achtergrondgeluid (bijv. een spotify playlist)?
        "}
        """,
        question_type="mc_yes_no" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well with a break every 30 minutes
        ",
        "nl":"
            Studeer je goed met een pauze elke 30 minuten?
        "}
        """,
        question_type="mc_yes_no" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well with a break every hour?
        ",
        "nl":"
            Studeer je goed met een pauze elk uur?
        "}
        """,
        question_type="mc_yes_no" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Do you study well with a break every two hours
        ",
        "nl":"
            Studeer je goed met een pauze elke 2 uur?
        "}
        """,
        question_type="mc_yes_no" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
task_management_comments_1 = [
    MockComment(
        body="""
        {"en":"
            It goes without saying that it is important to study under the best conditions. However, all too often students study under conditions that do not bring out their best. In this exercise you will think about your ideal study conditions. In the table below, circle ‘YES’ to the conditions in which you concentrate best. Remember, it can be good to have a preference for more than one option. For example, you may study well in the afternoon and at night. This makes you more a study ‘all-rounder’. Make sure you are honest with yourself – for example, is the radio a help or a distraction?
        ",
        "nl":"
            Het is vanzelfsprekend dat studeren onder goede omstandigheden belangrijk is. Toch zijn er veel studenten die studeren in omstandigheden die niet ideaal zijn. In deze oefening ga je nadenken over wat jouw ideale studie-omstandigheden zijn. Hieronder kan je aangeven waar je wel of niet goed kan studeren. Onthoud dat het goed kan zijn om meerdere opties te hebben zodat je kan afwisselen. Misschien kan je bijvoorbeeld goed ’s middags studeren, maar ook ’s avonds. Zorg ervoor dat je eerlijk bent met jezelf – is het luisteren naar muziek echt helpend, of is het eigenlijk een afleiding?
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Task management? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Task management nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Where you answered ‘YES’ gives you an idea of the study conditions in which you believe you concentrate best. Aim to study under these conditions more. But remember: studying in less than ideal conditions is better than no study at all.
        ",
        "nl":"
            Waar je hebt aangegeven goed te kunnen studeren geeft je een idee wat jouw ideale studie-omstandigheden zijn en waar jij je het best kan concentreren. Probeer vaker te studeren onder die omstandigheden, maar onthoudt: studeren in niet ideale omstandigheden is altijd nog beter dan niet studeren.
        "}
        """,
        location=16
    )
]

task_management_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {task_management_name} 1: My best study conditions
        ",
        "nl":"
            {task_management_name} 1: Mijn ideale studie-omstandigheden
        "}}
        """,
    survey_type="action",
    construct_name=task_management_name,
    questions=task_management_questions_1,
    comments=task_management_comments_1
)

task_management_questions_2 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
task_management_comments_2 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Task Management? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Task management nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            There are many strategies to help you use your time more effectively. Below are three exercises to give you a few ideas to help you use your time better.
        ",
        "nl":"
            Er zijn veel verschillende strategieën die je kunnen helpen om je tijd nuttiger te gebruiken. Hieronder zijn drie oefeningen om je een aantal ideeën te geven waarmee jij je tijd beter kan besteden.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <table><thead><tr><th>Strategy</th><th>Exercise for you to do</th></tr></thead><tbody><tr><td>Write a 'to do' list and prioritize it</td><td><ul><li>On a separate sheet, write a list of the things you have to do for homework, assignments, and study tonight.</li><li>Put the number 1 next to the most important item (important in terms of marks or due date –you choose)</li><li>Put the number 2 next to the most important item and so on.</li><li>On your homework tonight start working at number 1 and work your way through.</li></ul>Every night you do this you are studying more effectively</td></tr><tr><td>Identify opportunities for multiple tasks. Multi-tasking is identifying opportunities to do two things at the same time.</td><td>On a separate sheet, write down some opportunities for multiple tasks in your life. (Eg. get a friendto quiz you while doing the dishes; rehearse your French vocab while jogging)</td></tr><tr><td>Recognize in-between time and use it. In-between time is time between other tasks you are doing.<br/><br/><i>Concept of ‘in-between time’ adapted from R. Fry (2000). How to study. New Jersey: Career Press</i></td><td>On a separate sheet, write down your in-between time in a typical day and list some of the things you can do in this time. (Eg. ad breaks on TV to make a quick phone call; if the bus is late proof-read an essay)</td></tr></tbody></table>
        ",
        "nl":"
            <table><thead><tr><th>Strategie</th><th>Oefening om te doen</th></tr></thead><tbody><tr><td>Maak een ‘to do list’ en prioriteer de onderdelen</td><td><ul><li>Maak een aparte lijst van de dingen die je voor opdrachten moet doen.</li><li>Prioriteer de onderdelen, schrijf een 1 bij de belangrijkste</li><li>Schrijf een 2 bij de daaropvolgend belangrijkste, enz.</li><li>Als je gaat studeren start je met nummer 1 en werk je door je prioriteitenlijst heen.</li></ul>Als je dit zo elke keer doet dat je gaat studeren gaat dat veel effectiever.</td></tr><tr><td>Herken mogelijkheden om meerdere taken tegelijk uit te voeren.</td><td>Maak een aparte lijst voor mogelijkheden om te multi-tasken (bijv. je laten overhoren terwijl je afwast, je Engels oefenen terwijl je hardloopt)</td></tr><tr><td>Herken de ‘in-between times’, de tijd tussen 2 taken in.<br/><br/><i>Concept of ‘in-between time’ adapted from R. Fry (2000). How to study. New Jersey: Career Press</i></td><td>Maak een aparte lijst en schrijf op wanneer jouw dagelijkse in-between momenten zijn, en wat je in deze tijd zou kunnen doen. (Bijv. een samenvatting doorlezen terwijl je op de bus wacht)</td></tr></tbody></table>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            If you add up the study time you gain by using these three strategies you will find that by the end of the year you will have done weeks of extra university work and study without even feeling it
        ",
        "nl":"
            Als je de hoeveelheid studietijd optelt van deze drie strategieen kan je aan het eind van het jaar veel beter je studie doorlopen en zelfs extra studieopdrachten doen, zonder dat het je veel tijd kost.
        "}
        """,
        location=0
    )
]

task_management_2 = MockExercise(
    survey_title=f"""
        {{"en":"
            {task_management_name} 2: Using my time better
        ",
        "nl":"
            {task_management_name} 2: Mijn tijd beter gebruiken
        "}}
        """,
    survey_type="action",
    construct_name=task_management_name,
    questions=task_management_questions_2,
    comments=task_management_comments_2
)

task_management_questions_3 = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How did this exercise help you working on your learning goal?
        ",
        "nl":"
            Hoe heeft deze oefening je geholpen bij het behalen van je leerdoel?
        "}
        """,
        question_type="open"
    )
]
task_management_comments_3 = [
    MockComment(
        body="""
        {"en":"
            (Do you remember your learning goal for Task Management? If not, re-read it before doing this exercise.)
        ",
        "nl":"
            (Heb je je leerdoel voor Task management nog scherp? Als dat niet zo is, lees die dan nog even door voordat je aan deze oefening begint)
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            Another way to manage your study better is to develop a weekly study timetable. In this exercise you will draw up a timetable you can use through the week. Remember, it doesn’t have to be identical to the one below but this is a good start. The table below isan example of a first yearstudent’s timetable accounting for 20 study/assignmenthours with a minimum of 4.5hours on each subject each week.
        ",
        "nl":"
            Een andere manier om je studie beter te managen is door een wekelijks studieschema te maken. In deze oefening ga je een schema maken die je door de week kan gebruiken. Onthoud dat deze niet hetzelfde hoeft te zijn als hieronder, maar het kan wel een goede start zijn. Hieronder is een voorbeeld van een eerstejaars student met 20 studie-uur met een minimum van 4,5 uur voor elk onderwerp per week.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <ul><li>Draw up a timetable with details that reflect your own life, sport, work commitments, and other activities.</li><li>The timetable must be realistic (not too tough or too easy) but push you a little further whenever possible (eg. do a 2 hour study session rather than a 1 hour session).</li><li>If your circumstances change (eg. you drop your part-time job) then revise your timetable.</li><li>If you already have a study timetable that you feel is working well, use this time to read a chapter listed on the first page of this week’s exercises</li></ul>
        ",
        "nl":"
            <ul><li>Maak zelf een vergelijkbaar studieschema waar de details van jouw leven (sport, werk, andere activiteiten) in opgenomen zijn. </li><li>Het studieschema moet realistisch blijven (niet te moeilijk of te makkelijk), maar je wel elke week uitdagen om aan de slag te gaan.</li><li>Als de omstandigheden veranderen (bijv. Stoppen met een bijbaan) kan je je studieschema updaten.</li><li>Als de omstandigheden veranderen (bijv. Stoppen met een bijbaan) kan je je studieschema updaten.</li></ul>
        "}
        """,
        location=0
    )
]

task_management_3 = MockExercise(
    survey_title=f"""
        {{"en":"
            {task_management_name} 3: A weekly study timetable
        ",
        "nl":"
            {task_management_name} 3: Een wekelijks studieschema
        "}}
        """,
    survey_type="action",
    construct_name=task_management_name,
    questions=task_management_questions_3,
    comments=task_management_comments_3
)

task_management_questions_prepare = [
    MockQuestion(
        body="""
        {"en":"
            Which general rule(s) are most relevant for you, and what would you like to work on?
        ",
        "nl":"
            Welke algemene tip is voor jou het meest relevant en waar zou je aan willen werken?
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Specific
        ",
        "nl":"
            Specifiek
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Measurable
        ",
        "nl":"
            Meetbaar
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Achievable
        ",
        "nl":"
            Acceptabel
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Realistic
        ",
        "nl":"
            Realistisch
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            Timed
        ",
        "nl":"
            Tijdsgebonden
        "}
        """,
        question_type="open",
        required=False
    ),
    MockQuestion(
        body="""
        {"en":"
            OR: Choose a learning goal that fits your needs:<br/><ol><li>Learn to identify your ideal study conditions</li><li>Learn to look at ways you can use your study time better </li><li>Learn to develop a weekly study timetable</li></ol>
        ",
        "nl":"
            Of kies een leerdoel dat het best bij jou past:<br/><ol><li>Leer je ideale studieomstandigheden te identificeren.</li><li>Leer manieren om je studietijd beter te gebruiken.</li><li>Leer om een wekelijkst studieschema te maken.</li></ol>
        "}
        """,
        question_type="open",
        required=False
    ),
]
task_management_comments_prepare = [
    MockComment(
        body="""
        {"en":"
            Task management is the way you use your study time, organize your study timetable, and choose and arrange where you study. If you manage your study you tend to study in places where you can concentrate, use your study time well, and plan and stick to a study timetable.
        ",
        "nl":"
            Task management is de manier waarop jij je studietijd indeelt, hoe je een studieschema organiseert, en hoe jij je werkplek kiest en indeelt. Wanneer je het studeren goed managed gaat dit waarschijnlijk efficiënter. Dit kan je doen door te studeren op plaatsen waar je je kan concentreren, je tijd goed te gebruiken zonder afgeleid te worden, en je te houden aan een studieschema
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <u>General Rules</u> for task management:<br/><ul><li>Keep a record of what you do with your study time in a week. Record details about where you study, with whom, at what times, and under what conditions</li><li>Identify when and where you study best and study under these conditions more often</li><li>Draw up a study timetable for when, what, and where you will study. Make sure it is realistic. If the timetable is too difficult you are less likely to stick to it and if it is too easy it may not be very helpful</li><li>Reward yourself for keeping to your study timetable. For example, after completing an evening of study, you might listen to a CD, watch a favorite television show, call a friend, or surf the Internet for a while</li></ul>
        ",
        "nl":"
            <u>Algemene tips</u> for task management:<br/><ul><li>Hou een logbook bij of maak een verslag van wat je met je studietijd doet in een week. Noteer details over waar je studeert, met wie, op welke tijden, en onder welke omstandigheden.</li><li>Identificeer waneer en waar jij het best studeert, en studeer vaker in die condities.</li><li>Maak een studieschema voor wanneer, wat, en waar je gaat studeren. Zorg ervoor dat dit realistisch is. Als het te moeilijk of te veel is, is de kans groter dat je je er niet aan houdt. Als het te makkelijk is, heb je grote kans dat het niet veel nut heeft.</li><li>Beloon jezelf wanneer je je aan een studieschema hebt gehouden. Je kan na een avond studeren bijvoorbeeld wat muziek gaan luisteren, een serie streamen, of met vrienden afspreken.</li></ul>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            In the following exercise, you will set a learning goal for Task management. You can choose whether you want to formulate your own learning goal (1) or choose a learning goal from the list (2)
        ",
        "nl":"
            In deze oefening ga je leerdoelen stellen voor Task management. Je kan kiezen of je je eigen leerdoel wil formuleren (1), of je kan een leerdoel kiezen van de lijst (2).
        "}
        """,
        location=1
    ),
    MockComment(
        body="""
        {"en":"
            Formulate your own learning goal:<br/><br/>Set your personal goal with <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        ",
        "nl":"
            Formuleer je eigen leerdoel:<br/><br/>Stel je eigen doelen <a target='_blank' href='https://www.uu.nl/sites/default/files/upper_leerdoelen_smart_opstellen.pdf'>SMART</a>
        "}
        """,
        location=1
    )
]

task_management_prepare = MockExercise(
    survey_title=f"""
        {{"en":"
            Prepare: {task_management_name}
        ",
        "nl":"
            Voorbereiden: {task_management_name}
        "}}
        """,
    survey_type="prepare",
    construct_name=task_management_name,
    questions=task_management_questions_prepare,
    comments=task_management_comments_prepare
)

task_management_questions_reflect = [
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Which of the last three task management exercises do you think could be most helpful or useful to you? Exercise number:
        ",
        "nl":"
            Welk van de drie Task management oefeningen kan jou het meest helpen? Oefening Nummer:
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            List at least two things (try for a third) that this exercise taught you that you think will be most helpful to you.
        ",
        "nl":"
            Schrijf minstens twee (en probeer een derde) dingen op te schrijven wat deze oefening jou heeft geleerd en wat voor jou het meest nuttig is.
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Identify your ideal study conditions' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Herken je ideale studie omstandigheden’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Look at ways you can use your study time better' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Zoek naar manieren waarop jij je studietijd beter kan gebruiken’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            How does the message 'Develop a weekly study timetable' apply to you?
        ",
        "nl":"
            Hoe past de boodschap ‘Maak per week een studieschema ’ bij jou?
        "}
        """,
        question_type="open"
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            I believe I can apply what I’ve learnt in the exercises.
        ",
        "nl":"
            Wat ik geleerd heb in de oefeningen kan ik toepassen.
        "}
        """,
        question_type="likert_7" # !!!!!!!!!!!!! Not open
    ),
    MockQuestion(
        required=False,
        body="""
        {"en":"
            Thinking about the exercises you’ve made on Planning and your learning goal, what could be the next step for your learning process?
        ",
        "nl":"
            Als je terugkijkt op je leerdoel en de oefening(en) die je gemaakt hebt voor Task management, wat kan dan de volgende stap zijn in je leerproces?
        "}
        """,
        question_type="open"
    )
]
task_management_comments_reflect = [
    MockComment(
        body="""
        {"en":"
            Take a look at what you have written in the Action exercise(s). Reflecting and thinking about what you have learnt and what you found helpful can help you in the future.<br/><br/>Now work through the following questions. Remember, there is no right or wrong answer – just note what applies most to you.
        ",
        "nl":"
            Kijk terug op wat je hebt geschreven in de Task management Actie oefeningen. Reflecteer hierop, bedenk wat je hebt geleerd, en wat jou kan helpen in de toekomst.<br/><br/>Ga nu aan de slag met de volgende vragen. Onthoud dat er geen goede of foute antwoorden zijn – schrijf op wat voor jou het meest van toepassing is.
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            For each message, write out a specific way you can use it (e.g. “I’ll put careful and honest thought into when, where, and with whom I study best”)
        ",
        "nl":"
            Probeer voor elke boodschap op te schrijven hoe jij dat in de toekomst kan gebruiken (e.g. “Ik ga zorgvuldig en eerlijk kijken naar wanneer, waar en met wie ik het best kan studeren”)
        "}
        """,
        location=2
    )
]

task_management_reflect = MockExercise(
    survey_title=f"""
        {{"en":"
            Reflect: {task_management_name}
        ",
        "nl":"
            Reflecteren: {task_management_name}
        "}}
        """,
    survey_type="reflect",
    construct_name=task_management_name,
    questions=task_management_questions_reflect,
    comments=task_management_comments_reflect
)

task_management = [task_management_1, task_management_2, task_management_3, task_management_prepare, task_management_reflect]
#endregion

#region interpersonal_group_work_skills
interpersonal_group_work_skills_questions_1 = []
interpersonal_group_work_skills_comments_1 = [
    MockComment(
        body="""
        {"en":"
            Collaborating in a group does not only revolve around executing task, there is also an interpersonal component to keep in mind.<br/><br/>General tips to prevent group conflicts and uneven contributions:<br/><ul><li>Set up clear guidelines and work expectations at the beginning of the group project.</li><li>Assign roles and responsibilities so that each person will make an equal contribution.</li><li>Speak directly, but respectfully to the person who’s not completing their work.</li><li>Try not to let personal feelings impact your work in the group. Focus on the task. If personal feelings do get in the way however of group or individual performance, do address them directly, openly, and constructively, if needed seek professional guidance.</li><li>Address conflicts directly and respectfully.</li><li>Try and find common ground between ideas to reach reconciliation.</li><li>Value differences in opinions as opportunities to broaden the group’s perspective and improve the end results.</li></ul><br/>You can also take a look at the <a target='_blank' href='https://student.unsw.edu.au/groupwork'>Guide to Group Work</a>
        ",
        "nl":"
            Samenwerken in een groep gaat niet alleen over het uitvoeren van een taak, er zit ook een belangrijke interpersoonlijke component aan.<br/><br/>Algemene tips om conflicten en onevenredige bijdrages te voorkomen:<br/><ul><li>Stel duidelijke richtlijnen en verwachtingen aan het begin van het project.</li><li>Verdeel rollen en verantwoordelijkheden zodat iedereen een even grote bijdrage gaat leveren</li><li>Wees direct maar respectvol wanneer iemand zijn/haar werk niet af heeft.</li><li>Probeer je gevoelens niet je werk te laten beïnvloeden, focus op de taak. Als persoonlijke gevoelens de individuele uitvoering beïnvloeden, bespreek het dan open, direct, en constructief. Als het nodig is, zoek dan extra ondersteuning van bijv. een docent.</li><li>Pak conflicten direct maar respectvol aan.</li><li>Probeer een gemeenschappelijke basis te vinden voor ideeën en de taakuitvoer</li><li>Waardeer verschillen in mening en perspectief, dit zijn mogelijkheden om het perspectief van de groep te verbreden en het verbeterd het eindresultaat.</li></ul><br/>Je kan ook nog kijken naar de<a target='_blank' href='https://student.unsw.edu.au/groupwork'>Guide to Group Work</a>
        "}
        """,
        location=0
    )
]

interpersonal_group_work_skills_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {interpersonal_group_work_skills_name}: General Tips
        ",
        "nl":"
            {interpersonal_group_work_skills_name}: General Tips
        "}}
        """,
    survey_type="action",
    construct_name=interpersonal_group_work_skills_name,
    questions=interpersonal_group_work_skills_questions_1,
    comments=interpersonal_group_work_skills_comments_1
)

# interpersonal_group_work_skills_questions_2 = []
# interpersonal_group_work_skills_comments_2 = []

# interpersonal_group_work_skills_2 = MockExercise(
#     survey_title=f"{interpersonal_group_work_skills_name} 2",
#     survey_type="action",
#     construct_name=interpersonal_group_work_skills_name,
#     questions=interpersonal_group_work_skills_questions_2,
#     comments=interpersonal_group_work_skills_comments_2
# )

# interpersonal_group_work_skills_questions_3 = []
# interpersonal_group_work_skills_comments_3 = []

# interpersonal_group_work_skills_3 = MockExercise(
#     survey_title=f"{interpersonal_group_work_skills_name} 3",
#     survey_type="action",
#     construct_name=interpersonal_group_work_skills_name,
#     questions=interpersonal_group_work_skills_questions_3,
#     comments=interpersonal_group_work_skills_comments_3
# )

# interpersonal_group_work_skills_questions_prepare = []
# interpersonal_group_work_skills_comments_prepare = []

# interpersonal_group_work_skills_prepare = MockExercise(
#     survey_title=f"Prepare: {interpersonal_group_work_skills_name}",
#     survey_type="prepare",
#     construct_name=interpersonal_group_work_skills_name,
#     questions=interpersonal_group_work_skills_questions_prepare,
#     comments=interpersonal_group_work_skills_comments_prepare
# )

# interpersonal_group_work_skills_questions_reflect = []
# interpersonal_group_work_skills_comments_reflect = []

# interpersonal_group_work_skills_reflect = MockExercise(
#     survey_title=f"Reflect: {interpersonal_group_work_skills_name}",
#     survey_type="reflect",
#     construct_name=interpersonal_group_work_skills_name,
#     questions=interpersonal_group_work_skills_questions_reflect,
#     comments=interpersonal_group_work_skills_comments_reflect
# )

# interpersonal_group_work_skills = [interpersonal_group_work_skills_1, interpersonal_group_work_skills_2, interpersonal_group_work_skills_3, interpersonal_group_work_skills_prepare, interpersonal_group_work_skills_reflect]
interpersonal_group_work_skills = [interpersonal_group_work_skills_1]
#endregion

#region task_group_work_skills
task_group_work_skills_questions_1 = []
task_group_work_skills_comments_1 = [
    MockComment(
        body="""
        {"en":"
            In order to work effectively as a group, assigning group roles and division of labour is critical. The following list is not exhaustive, but it can be a starting place of assigning roles to suit your group’s needs. Taking and discussing these 5 steps can help to do so:
        ",
        "nl":"
            Om als groep goed te kunnen samenwerken, is het verdelen van rollen en taken cruciaal. De volgende lijst is niet allesomvattend, maar kan wel het startpunt zijn om rollen te verdelen voor jouw groep. Doe dit door deze 5 stappen te nemen en dit te bespreken:
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <ol><li><b>Assign roles.</b> See examples of roles below.</li><li><b>Create a timeline.</b> A timeline is important to make sure the project isn’t left until the last minute.</li><li><b>Divide projects into chunks.</b> Distribute work between members to make it less overwhelming. This also makes it easier to complete because group members can work independently on their sections.</li><li><b>Schedule meetings.</b> Group meetings could be in person or use virtual technology such as Skype or chat applications. Sometimes projects can be organized mostly via email which makes it easy to share notes and research.</li><li><b>Create a communication plan.</b> No matter how you organize your communication, it is important to set mutually agreed ground rules for contribution. For example, if you miss a meeting you could be expected to read and respond to notes taken at the meeting within 24 hours. Or, if you consistently miss meetings/fail to communicate/produce work, you may not be given credit for the project. That being said, life happens. Put yourself in the shoes of your group members. Try and understand their perspective and be inclusive as much as possible.</li></ol>
        ",
        "nl":"
            <ol><li><b>Spreek rollen af.</b> Zie hieronder wat voorbeelden.</li><li><b>Maak een tijdlijn of planning.</b> Een tijdlijn is belangrijk om zeker te weten dat er geen onderdelen last minute gedaan moeten worden. </li><li><b>Verdeel projecten in behapbare onderdelen.</b> Verdeel werk tussen groepsleden om het minder overweldigend te laten zijn. Dit maakt het ook makkelijker om af te maken, omdat groepsleden onafhankelijk aan hun gedeelte kunnen werken.</li><li><b>Plan bijeenkomsten.</b> Groepsbijeenkomsten kunnen fysiek of online plaatsvinden, soms kan het ook via email zodat je gemakkelijk notities en literatuur kan delen.</li><li><b>Schrijf een communicatieplan.</b> Het maakt niet uit hoe je je communicatie organiseert, als de afspraken maar door iedereen gedragen worden. Als je bijvoorbeeld een bijeenkomst mist kan er verwacht worden dat je de notities van de bijeenkomst gelezen hebt voor de volgende bijeenkomst. Dat gezegd hebbende, overkomen je soms ook dingen. Probeer je te verplaatsen in je groepsgenoten en hun perspectief te begrijpen.</li></ol>
        "}
        """,
        location=0
    ),
    MockComment(
        body="""
        {"en":"
            <ol><li>Leader<ol><li>Leads discussion with open-ended questions</li><li>Encourages all group members</li><li>Facilitates brainstorming by summarizing and clarifying group comments</li><li>Helps guide conversation and focuses on positive statements</li><li>Checks for consensus or questions from group members</li></ol></li><li>Organizer<ol><li>Schedules meetings</li><li>Keeps the project on track</li><li>Thinks about the ‘big picture’</li><li>Ensures meetings follow a timeline/agenda</li><li>Takes notes at meetings to send to everyone afterwards</li></ol></li><li>Editor(s)<ol><li>Edits completed work</li><li>Compiles different pieces of reports/presentations from different group members to create ‘flow’ and consistency</li></ol></li><li>Trouble-Shooter/Brainstormer<ol><li>Thinks about positive/negatives of ideas presented by the group</li><li>Thinks about possible solutions to problems</li><li>Critiques project based on assignment expectations/rubric to ensure success</li></ol></li></ol>
        ",
        "nl":"
            <ol><li>Leider<ol><li>Leidt de discussie met open vragen </li><li>Moedigt groepsleden aan </li><li>Faciliteert het brainstormen door samen te vatten en opmerkingen te verduidelijken</li><li>Helpt het gesprek op de juiste koers te houden en focust op positieve statements </li><li>Kijkt of er consensus vanuit de groep of dat er nog vragen zijn.</li></ol></li><li>Organisator<ol><li>Plant de bijeenkomsten</li><li>Houdt het project op koers</li><li>Denkt na over de lange termijn</li><li>Houd de agenda voor de bijeenkomst in de gaten</li><li>Maakt notities van de bijeenkomst en stuurt die rond naderhand.</li></ol></li><li>Editor(s)<ol><li>Maakt de laatste wijzigingen in het gemaakte werk</li><li>Voegt de verschillende onderdelen van een opdracht samen en zorgt voor een goede ‘flow’ en eenduidigheid.</li></ol></li><li>Trouble-Shooter/Brainstormer<ol><li>Denkt na over positieve of negatieve ideeën die door groepsgenoten gegeven worden</li><li>Denkt na over mogelijke oplossingen</li><li>Geeft opbouwende kritiek op basis van de opdrachtomschrijving en rubric zodat daaraan voldaan wordt.</li></ol></li></ol>
        "}
        """,
        location=0
    ),
]

task_group_work_skills_1 = MockExercise(
    survey_title=f"""
        {{"en":"
            {task_group_work_skills_name} 1: Get organized
        ",
        "nl":"
            {task_group_work_skills_name} 1: Organizeren
        "}}
        """,
    survey_type="action",
    construct_name=task_group_work_skills_name,
    questions=task_group_work_skills_questions_1,
    comments=task_group_work_skills_comments_1
)

# task_group_work_skills_questions_2 = []
# task_group_work_skills_comments_2 = []

# task_group_work_skills_2 = MockExercise(
#     survey_title=f"{task_group_work_skills_name} 2",
#     survey_type="action",
#     construct_name=task_group_work_skills_name,
#     questions=task_group_work_skills_questions_2,
#     comments=task_group_work_skills_comments_2
# )

# task_group_work_skills_questions_3 = []
# task_group_work_skills_comments_3 = []

# task_group_work_skills_3 = MockExercise(
#     survey_title=f"{task_group_work_skills_name} 3",
#     survey_type="action",
#     construct_name=task_group_work_skills_name,
#     questions=task_group_work_skills_questions_3,
#     comments=task_group_work_skills_comments_3
# )

# task_group_work_skills_questions_prepare = []
# task_group_work_skills_comments_prepare = []

# task_group_work_skills_prepare = MockExercise(
#     survey_title=f"Prepare: {task_group_work_skills_name}",
#     survey_type="prepare",
#     construct_name=task_group_work_skills_name,
#     questions=task_group_work_skills_questions_prepare,
#     comments=task_group_work_skills_comments_prepare
# )

# task_group_work_skills_questions_reflect = []
# task_group_work_skills_comments_reflect = []

# task_group_work_skills_reflect = MockExercise(
#     survey_title=f"Reflect: {task_group_work_skills_name}",
#     survey_type="reflect",
#     construct_name=task_group_work_skills_name,
#     questions=task_group_work_skills_questions_reflect,
#     comments=task_group_work_skills_comments_reflect
# )

# task_group_work_skills = [task_group_work_skills_1, task_group_work_skills_2, task_group_work_skills_3, task_group_work_skills_prepare, task_group_work_skills_reflect]
task_group_work_skills = [task_group_work_skills_1]
#endregion

all_exercises = [anxiety, failure_avoidance, uncertain_control, self_sabotage, disengagement, self_belief, learning_focus, valuing, persistence, planning, task_management, interpersonal_group_work_skills, task_group_work_skills]
