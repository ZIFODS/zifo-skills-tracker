from urllib.parse import quote as url_encode


class GetAllConsultants:
    """
    no input required
    """

    QUERY_PATH = "/consultants/"
    EXPECTED_RESULT = {
        "items": [
            {
                "name": "Adam Price",
                "email": "adam_price@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Aled Jones",
                "email": "aled_jones@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Alex Jones",
                "email": "alex_jones@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Alun Wyn Jones",
                "email": "alun_wyn_jones@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Anthony Hopkins",
                "email": "anthony_hopkins@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Bonnie Tyler",
                "email": "bonnie_tyler@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Bryn Parry-Jones",
                "email": "bryn_parry-jones@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Bryn Terfel",
                "email": "bryn_terfel@gmail.com",
                "type": "Consultant",
            },
            {"name": "Budgie", "email": "budgie@gmail.com", "type": "Consultant"},
            {
                "name": "Catherine Zeta-Jones",
                "email": "catherine_zeta-jones@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Cerys Matthews",
                "email": "cerys_matthews@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Charlotte Church",
                "email": "charlotte_church@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Christian Bale",
                "email": "christian_bale@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Colin Jackson",
                "email": "colin_jackson@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "David Emanuel",
                "email": "david_emanuel@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Derek Brockway",
                "email": "derek_brockway@gmail.com",
                "type": "Consultant",
            },
            {"name": "Duffy", "email": "duffy@gmail.com", "type": "Consultant"},
            {
                "name": "Ellie Goulding",
                "email": "ellie_goulding@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Gareth Bale",
                "email": "gareth_bale@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Gareth Thomas",
                "email": "gareth_thomas@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Geraint Thomas",
                "email": "geraint_thomas@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Gethin Jones",
                "email": "gethin_jones@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Glynis Johns",
                "email": "glynis_johns@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Gwyneth Powell",
                "email": "gwyneth_powell@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Huw Edwards",
                "email": "huw_edwards@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Ioan Gruffudd",
                "email": "ioan_gruffudd@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Iwan Rheon",
                "email": "iwan_rheon@gmail.com",
                "type": "Consultant",
            },
            {"name": "John Cale", "email": "john_cale@gmail.com", "type": "Consultant"},
            {
                "name": "Katherine Jenkins",
                "email": "katherine_jenkins@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Kiri Te Kanawa",
                "email": "kiri_te_kanawa@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Leigh Halfpenny",
                "email": "leigh_halfpenny@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Matthew Rhys",
                "email": "matthew_rhys@gmail.com",
                "type": "Consultant",
            },
            {"name": "Max Boyce", "email": "max_boyce@gmail.com", "type": "Consultant"},
            {
                "name": "Michael Sheen",
                "email": "michael_sheen@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Nerys Hughes",
                "email": "nerys_hughes@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Nigel Owens",
                "email": "nigel_owens@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Owain Yeoman",
                "email": "owain_yeoman@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Ray Milland",
                "email": "ray_milland@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Rhod Gilbert",
                "email": "rhod_gilbert@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Richard Burton",
                "email": "richard_burton@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Rob Brydon",
                "email": "rob_brydon@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Rob Howley",
                "email": "rob_howley@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Ruth Jones",
                "email": "ruth_jones@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Ryan Davies",
                "email": "ryan_davies@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Ryan Giggs",
                "email": "ryan_giggs@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Shirley Bassey",
                "email": "shirley_bassey@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Sian Lloyd",
                "email": "sian_lloyd@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Sian Phillips",
                "email": "sian_phillips@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Tanni Grey-Thompson",
                "email": "tanni_grey-thompson@gmail.com",
                "type": "Consultant",
            },
            {
                "name": "Taron Egerton",
                "email": "taron_egerton@gmail.com",
                "type": "Consultant",
            },
            {"name": "Tom Ellis", "email": "tom_ellis@gmail.com", "type": "Consultant"},
            {"name": "Tom Jones", "email": "tom_jones@gmail.com", "type": "Consultant"},
        ]
    }


class GetSingleConsultant:
    """
    input: single consultants' email (existing) and name of consultant corresponding to INPUT (existing, required for
           expected result)
    """

    INPUT = "duffy@gmail.com"
    INPUT_NAME = "Duffy"
    QUERY_PATH = f"/consultants/{url_encode(INPUT)}"
    EXPECTED_RESULT = {"name": INPUT_NAME, "email": INPUT, "type": "Consultant"}


class GetSingleConsultantNotFound:
    """
    input: single consultants' name (not existing)
    """

    INPUT = "test-guy@test.com"
    QUERY_PATH = f"/consultants/{url_encode(INPUT)}"
    EXPECTED_DETAIL = "Consultant not found"


class CreateDuplicateConsultant:
    """
    input: single consultants' email and name (existing)
    """

    INPUT_MAIL = "duffy@gmail.com"
    INPUT_NAME = "Duffy"
    INPUT = {"name": INPUT_NAME, "email": INPUT_MAIL}
    QUERY_PATH = "/consultants/"
    EXPECTED_DETAIL = "Consultant already exists"


class DeleteConsultantNotFound:
    """
    input: single consultants' email (not existing)
    """

    INPUT = "test-guy@test.com"
    QUERY_PATH = f"/consultants/{url_encode(INPUT)}"
    EXPECTED_DETAIL = "Consultant not found"


class CreateConsultant:
    """
    input: single consultants' email and name (existing)
    """

    INPUT_MAIL = "test-guy@test.com"
    INPUT_NAME = "TEST GUY"
    INPUT = {"name": INPUT_NAME, "email": INPUT_MAIL}
    QUERY_PATH = "/consultants/"
    EXPECTED_RESULT = {"name": INPUT_NAME, "email": INPUT_MAIL, "type": "Consultant"}


class CreateConsultantCheckResult:
    """
    input: same email as in CreateConsultant!
    """

    INPUT = CreateConsultant.INPUT_MAIL
    QUERY_PATH = f"/consultants/{url_encode(INPUT)}"
    EXPECTED_RESULT = CreateConsultant.EXPECTED_RESULT


class DeleteConsultant:
    """
    input: single consultants' email (existing)
    """

    INPUT = "duffy@gmail.com"
    QUERY_PATH = f"/consultants/{url_encode(INPUT)}"
    EXPECTED_MESSAGE = f"Deleted consultant {INPUT}"


class DeleteConsultantCheckResult:
    """
    input: same email as in DeleteConsultant!
    """

    INPUT = DeleteConsultant.INPUT
    QUERY_PATH = DeleteConsultant.QUERY_PATH
    EXPECTED_DETAIL = "Consultant not found"
