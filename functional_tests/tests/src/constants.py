#  Define the environment variable name who's value acts as the 'everything' token
#  Most likely you will never change this

token_all_products_no_restrictions = 'TOKEN_ALL_PRODUCTS_NO_RESTRICTIONS'

expected_bad_token_response = 'FORBIDDEN'

expected_value_out_of_range_response = 'INTERNAL_SERVER_ERROR'

expected_bad_input_response = 'BAD_USER_INPUT'

expected_syntax_error = 'Syntax error'

expected_failed_validation_error = 'GRAPHQL_VALIDATION_FAILED'

#  AOI as dict
aoi: dict = {'type': 'Polygon',
             'coordinates': [[[129.462890625, 35.53222622770337],
                              [89.736328125, 13.66733825965496],
                              [113.291015625, -50.17689812200105],
                              [171.337890625,  -49.32512199104001],
                              [171.6015625, -32.99023555965107],
                              [129.462890625,  35.53222622770337]
                              ]]}

aoi_a_for_token_limit_test: dict = {
    'type': 'Polygon',
    'coordinates': [
                    [
                        [-97, 31],
                        [-80, 31],
                        [-80, 17],
                        [-97, 17],
                        [-97, 31]
                    ]
    ]

}



#  BUILDING BLOCKS FOR FULL QUERY

total_count_segment = """
   totalCount{
      value
      relation
    }
 """

static_data_segment = """
staticData {
        aisClass
        flag
        name
        callsign
        timestamp
        updateTimestamp
        shipType
        shipSubType
        mmsi
        imo
        callsign
        dimensions {
          a
          b
          c
          d
          width
          length
        }
      }
"""

last_position_update_segment = """
lastPositionUpdate {
        accuracy
        collectionType
        course
        heading
        latitude
        longitude
        maneuver
        navigationalStatus
        rot
        speed
        timestamp
        updateTimestamp
      }
"""

current_voyage_segment = """
currentVoyage {
        destination
        draught
        eta
        timestamp
        updateTimestamp
      }
"""

characteristics_basic_segment = """
      characteristics{
        basic{
          capacity{
            deadweight
          } # capacity
          vesselTypeAndTrading{
            vesselSubtype
          } # vesselTypeAndTrading
          history{
            builtYear
          } # history
        } # basic
      }# characteristics
"""

characteristics_extended_segment = """
characteristics{
                        basic{
                          capacity{
                            deadweight
                          } # capacity
                          history{
                            builtYear
                          } # history
                        }
                        extended{
                          capacity{
                            cars
                            deadweight
                            hatchCount
                            holdCount
                            holdDimensions
                            hatchDimensions
                            laneMeters
                            passengers
                            grossTonnage
                            displacement
                            grainCubicCapacity
                            reeferCubic
                            liquidCubic98Percent
                            cars
                            tpcmi
                            reeferCubic
                            liquidCubic98Percent
                            teu
                            feu
                            teu14t
                            teuSurplus
                            tpcmi
                          } # capacity
                          dimensions{
                            airDraught
                            draught
                            beamMoulded
                            lengthOverall
                            keelToManifold
                            berthCount
                            depth
                          } # dimensions
                          registration{
                            iceClass
                            class1Code
                            class2Code
                            classDetails
                            isIceClassed
                            certificates
                          } # registration
                          history{
                            deadYear
                            builtYear
                            launchYear
                            keelLaidYear
                            vesselNameDate
                            hullNumber
                            shipBuilder
                            registeredOwner
                          } # history
                          propulsion{
                            mainEngineCount
                            engineDesignation
                            mainEngineDesigner
                            bowThrusterCount
                            mcoKw
                            mcoHp
                            mcoRpm
                            propellerCount
                            sternThrusterCount
                            propulsionType
                            propellerType
                          } # propulsion
                          bunker{
                            bunkers{
                              capacity
                              tankCount
                              fuelTypeCode
                              fuelUnitCode
                            }
                            range
                          } # bunker
                        } # extended
                      } # characteristics


"""

imo_with_characteristics = [9809643, 9340984, 9120853]
mmsi_with_characteristics = [341991000, 533051600, 271000588]