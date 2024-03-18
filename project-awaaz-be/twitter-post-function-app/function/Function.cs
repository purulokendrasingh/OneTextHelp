using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Azure.WebJobs.Extensions.SignalRService;
using System.Collections.Generic;
using Microsoft.Azure.Documents;
using Microsoft.Extensions.Logging;

namespace CSharp
{
    public static class Function
    {
        [FunctionName("negotiate")]
        public static SignalRConnectionInfo Negotiate(
            [HttpTrigger(AuthorizationLevel.Anonymous)] HttpRequest req,
            [SignalRConnectionInfo(HubName = "serverless")] SignalRConnectionInfo connectionInfo)
        {
            return connectionInfo;
        }

        [FunctionName("broadcast")]        
        public static async Task Run([CosmosDBTrigger(
        databaseName: "OneTextHelp",
        collectionName: "MessageDetails",
        ConnectionStringSetting = "CosmosDBConnectionString",
        LeaseCollectionName = "leases",
        CreateLeaseCollectionIfNotExists =true)]IReadOnlyList<Document> input, ILogger log,
        //SignalR output Binding
        [SignalR(HubName = "serverless")] IAsyncCollector<SignalRMessage> signalRMessages)
        {
            if (input != null && input.Count > 0)
            {
                var result = new CosmosResult{
                    name = input[0].GetPropertyValue<string>("name"),
                    phone = input[0].GetPropertyValue<string>("phone"),
                    message = input[0].GetPropertyValue<string>("message"),
                    TweetId = input[0].GetPropertyValue<string>("TweetId")
                };
                await signalRMessages.AddAsync(new SignalRMessage
                {
                    Target = "target",
                    Arguments = new[] { result }
                });
            }
        }

        class CosmosResult
        {
            public string name { get; set; }
            public string phone { get; set; }
            public string message { get; set; }
            public string TweetId { get; set; }
        }
    }
}