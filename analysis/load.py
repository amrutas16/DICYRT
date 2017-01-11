import sys,cass,config

sys.dont_write_bytecode=True
from setting_logs import set_log

if __name__=="__main__":
	set_log("INFO", "logs", "Loading Business_details from" + str(config.businesslist))
	cass.insert_business_details(config.businesslist)

