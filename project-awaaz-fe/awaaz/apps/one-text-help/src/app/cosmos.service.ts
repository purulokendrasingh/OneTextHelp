import { CosmosClient } from '@azure/cosmos';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class CosmosService {
  key = "7HiKsFpk7hRsMBxLNg6yFGlaamf0LHCJiWAoYaAxjp37R87Vj9l2flxROd0yijj0Lq2nYDWBpMEh6Rb2Bi6EHA==";
  endpoint = "https://ash-project-awaaz.documents.azure.com:443/";
  containerId = "MessageDetails";
  databaseId = "OneTextHelp";

  public async getProjects(): Promise<any>{
    const client = new CosmosClient({endpoint: this.endpoint, key: this.key});
    const database = client.database(this.databaseId);
    const container = database.container(this.containerId);
    const querySpec = {query: "SELECT * from c "};
    const { resources:items } = await container.items.query(querySpec).fetchAll();
    return items;
  }
}
