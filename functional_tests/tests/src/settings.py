
# #  Comment / Uncomment to set the endpoint
# #  PRODUCTION
# endpoint = 'https://api.spire.com/graphql'

#  STAGING
endpoint = 'https://api.staging.maritime.spire.sh/graphql'

# STAGING CANARY
#  endpoint = 'https://api.staging.maritime.spire.sh/graphql/canary'

#  PRODUCTION CANARY
#  endpoint = 'https://api.spire.com/graphql/canary'

#  CONNECTIVITY SETTINGS
#  HOW LONG TO WAIT IN SECONDS TO TIME OUT
#  RECOMMENDATION: SET TIME OUT > 30 FOR predictedVesselRoute support
timeout = 30

#  HOW MANY TIMES TO RETRY CONNECTION BEFORE ERRORING OUT
retries = 3

#  For tests that will page through a lot of pages, optionally stop paging by setting this
#  0 means there is no limit and paging will go through every single page
#  WARNING: changing this may produce false positives,
#  it is useful for debugging tests when you don't want them to run long
page_limit = 0
