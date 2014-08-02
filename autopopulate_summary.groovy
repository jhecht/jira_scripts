/* SYSAPP-74 - This groovy script auto-populates the issue summary with the following: 
"Product; Genre; Min. Target Age - Max. Target Age; Gender; Start Date - End Date"
Used in THEOREM project for Avails Sub-Task as a post-function on create.*/ 

import com.atlassian.jira.ComponentManager
import com.atlassian.jira.issue.CustomFieldManager
import com.atlassian.jira.issue.MutableIssue
import com.atlassian.jira.issue.Issue
import com.atlassian.jira.issue.customfields.view.CustomFieldParams
import com.atlassian.jira.issue.fields.CustomField
import java.util.HashMap

ComponentManager componentManager = ComponentManager.getInstance()
Issue issue = issue;
CustomFieldManager customFieldManager = componentManager.getCustomFieldManager()

CustomField cf1 = (CustomField) customFieldManager.getCustomFieldObjectByName("Product")

CustomField cf2 = customFieldManager.getCustomFieldObjectByName("Genre");

CustomField cf3 = customFieldManager.getCustomFieldObjectByName("Min. Target Age");

CustomField cf4 = customFieldManager.getCustomFieldObjectByName("Max. Target Age");

CustomField cf5 = customFieldManager.getCustomFieldObjectByName("Gender");

//This is the Start Date custom field
CustomField cf6 = customFieldManager.getCustomFieldObject(12994);

CustomField cf7 = customFieldManager.getCustomFieldObjectByName("End Date");


CustomFieldParams productValue = issue.getCustomFieldValue(cf1) as CustomFieldParams;

String genreValue = issue.getCustomFieldValue(cf2).toString();

int minAgeValue = issue.getCustomFieldValue(cf3).toInteger();

int maxAgeValue = issue.getCustomFieldValue(cf4).toInteger();

//String agerangeValue = issue.getCustomFieldValue(cf3).toString();

genderValue = issue.getCustomFieldValue(cf5)?.getValue();

startdateValue = issue.getCustomFieldValue(cf6)?.getDateString();

enddateValue = issue.getCustomFieldValue(cf7)?.getDateString();


if (productValue) {
    String parentValue  = issue.getCustomFieldValue(cf1).get(null)
    String childValue = issue.getCustomFieldValue(cf1).get("1")
    
    if (issue.summary){
	if(childValue && genreValue != "null"){
    		issue.summary = issue.summary + " -  " + parentValue + " /  " + childValue + "; " + genreValue + "; " + minAgeValue + "-" + maxAgeValue + "; " + genderValue + "; " + startdateValue + " - " + enddateValue;
		}	
	else if (genreValue != "null"){
    		issue.summary = issue.summary + " -  " + parentValue  + "; " + genreValue + "; " + minAgeValue + "-" + maxAgeValue + "; " + genderValue + "; " + startdateValue + " - " + enddateValue;
		}
	else if(childValue){
	    	issue.summary = issue.summary + " -  " + parentValue + " /  " + childValue + "; " + minAgeValue + "-" + maxAgeValue + "; " + genderValue + "; " + startdateValue + " - " + enddateValue;}
	else {
    		issue.summary = issue.summary + " -  " + parentValue + "; " + minAgeValue + "-" + maxAgeValue + "; " + genderValue + "; " + startdateValue + " - " + enddateValue;
	}
}
}
