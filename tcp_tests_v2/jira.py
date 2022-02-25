from atlassian import Jira
import shared
from loguru import logger
logger.add('logs/jira.log', format='{time} {name} {message}', level='DEBUG',
           retention="10 days")

class JiraTools:

    def __init__(self, label):
        self.jira = Jira(
            url='https://spireglobal.atlassian.net',
            username="bruce.bookman@spire.com",
            password="HJs0GizKO7eoyMOVXaL42B4F",
            cloud=True)
        self.label = label


    def set_status(self, issue_key, status_name):
        self.jira.set_issue_status(issue_key=issue_key, status_name=status_name)

    def set_comment(self, issue_key, comment):
        self.jira.issue_add_comment(issue_key, comment)

    def get_status(self, issue_id):
        # get_issue_status
        return self.jira.get_issue_status(issue_id)

    def add_comment(self, issue_id, comment):
        self.jira.issue_add_comment(issue_id, comment)

    def get_summary(self, issue_id):
        issue = self.jira.issue(issue_id)
        summary = issue['fields']['summary']
        return summary

    def new_issue(self, summary='default summary',
                  description='default description',
                  epic_link='MDO-218',
                  status='Fail',
                  assignee='bruce.bookman@spire.com'):
        if shared.update_jira:
            issue_dict = {
                'project': {
                            'key': 'MDO'},
                'summary': summary,
                'description': description,
                'issuetype': {'name': 'Task'},
                'customfield_10014': epic_link,
                'assignee': assignee,
            }

            new_issue = self.jira.create_issue(fields=issue_dict)
            new_key = new_issue['key']
            issue = self.jira.issue(new_key)
            #issue.fields.labels.append(self.label)
            #issue.update(fields={"labels": issue.fields.labels})
            self.jira.issue_transition(new_key, status)
            string = [f'{k}:{v}\n' for k, v in new_issue.items()]
            info = f"""
            SUMMARY: {summary}
            DESCRIPTION: {description}
            EPIC: {epic_link}
            STATUS: {status}
            ASSIGNEE: {assignee}
            LABEL: {self.label}
            {string}
            """
            logger.debug(f"""
            NEW JIRA ISSUE CREATED
            {info}""")
        else:
            logger.info('SKIPPING JIRA UPDATE BY REQUEST')

