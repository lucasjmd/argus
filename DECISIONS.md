## General<br>
**Folder architecture**<br>
I organised my folders into adapters and domain. This decouples business logic from infrastructure. The code that <br>
dictates what constitutes a transaction and its rule are separate from the system that allows the data to come in.

**Tools**<br>
Ruff<br>
UV

## Code
### Domain
<code>**base.py**</code><br>
I chose to use an abstract base class for <code>BaseIngestor</code> because this acts as a contract that validates 
how related classes will be built. It acts as a framework. For example, we define that any child ingestor class must have a <code>get_transactions</code>
method that yields a generator object.<br><br>

<code>**validation_models.py**</code><br>
I use the Pydantic package to validate the data. It defines the schema of the data subsequent logic expects. It also is<br>
extremely fast which prepares us for high-volumes of financial transactions passing through.<br>

We use a constrained decimal type to avoid floating point errors in transaction amounts.<br>

We validate account names and check that the amounts are reasonable with various constraints.<br>

### Adapters
<code>**ingestors.py**</code><br>
We want the <code>get_transactions</code> method to yield an iterator as using a list would read the data into memory. 
The simulated data we are using is large enough to cause performance issues. It keeps the momory footprint constant (`O(1)`).<br>

We use the <code>chain</code> method from <code>itertools</code> to peek into an iterator at the first item (to validate)<br>
it contains data, without destroying the item if it wasn't empty (which would delete our first transaction).<br><br>


