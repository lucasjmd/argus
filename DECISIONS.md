<code>base.py</code><br>
I chose to use an abstract base class for <code>BaseIngestor</code> because this acts as a contract that validates 
how related classes will be built. For example, we define that any child ingestor class must have a <code>get_transactions</code>
method that yields a generator object.<br><br>

We want the <code>get_transactions</code> method to yield an iterator as using a list would read the data into memory. 
The simulated data we are using is large enough to cause performance issues.

<code>validation_models.py</code><br>
I use the Pydantic package to validate the data. It defines the schema of the data subsequent logic expects.<br><br>
