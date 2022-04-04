import flwr as fl
import sys
import flwr as fl
import numpy as np

class SaveModelStrategy(fl.server.strategy.FedAvg):
    
    def aggregate_fit(self,rnd,results,failures): 
        print("hi")       
        aggregated_weights = super().aggregate_fit(rnd, results, failures) # default aggregation
        if aggregated_weights is not None:
            # print(f"Saving round {rnd} aggregated_weights...")
            np.savez("round-{}-weights.npz".format(rnd) ,aggregated_weights)
        return aggregated_weights

# Create strategy and run server
strategy = SaveModelStrategy()

# Start Flower server for three rounds of federated learning
fl.server.start_server(
        server_address = 'localhost:'+str(sys.argv[1]) , 
        config={"num_rounds": 2} ,
        grpc_max_message_length = 1024*1024*1024,
        strategy = strategy
)