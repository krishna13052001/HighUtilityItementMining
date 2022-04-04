import sys
import flwr as fl
import numpy as np

class SaveModelStrategy(fl.server.strategy.FedAvg):
    totalUtilityItemsets = set()
    def aggregate_evaluate(self,round_number,results,failures): #fit
        print("Total UtilityItemsets ",results)
        print("Results ",results,"Failures",failures)
        for i in range(len(results)):
            print(results[i][-1].metrics['accuracy'])
        sum,count = 0,0
        for i in range(len(results)):
            sum += results[i][-1].metrics['accuracy']
            count += 1
        print("Accuracy of the model was ", sum/count)
        return results
try:
    fl.server.start_server(server_address = 'localhost:'+str(sys.argv[1]) ,config={"num_rounds": 2} ,grpc_max_message_length = 1024*1024*1024,
    strategy = SaveModelStrategy())
except:
    pass