from helium import start_chrome, go_to, click
from helium import Text, TextField, ListItem, Button


class CrunchBaseScrapper:
    def __init__(self, headless=False):
        self.driver = start_chrome(headless=headless)

    def go_company_ranking(self, ranking):
        go_to(f"https://www.crunchbase.com/search/organization.companies/field/organizations/rank_org_company/{ranking}")
        if Text("Organization Name").exists():
            print(click(Button(below="Organization Name")))
            # print(TextField(below="Industries").value)
            # print(Text(below="Headquarters Location").value)


    def get_acquired_by(self):
        if Text('Acquired by').exists():
            print(Text(below="Acquired by").value)

    def get_about(self):
        print(Text(below='About').value)

    def get_name(self):
        pass


cbs = CrunchBaseScrapper()
cbs.go_company_ranking(1)
# cbs.get_acquired_by()
