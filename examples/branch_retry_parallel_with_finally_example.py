import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl
import awssl.ext

def branch_retry_parallel_state_example():

	finally_state = awssl.Pass(
		Name="MyFinally",
		Comment="This is the branch to execute as a 'finally' statement to the Parallel state",
		ResultAsJSON={"Finally": "Completed"},
		EndState=True)

	# Create the branch processing to be performed - in this case returning the name of the StartState
	p1 = awssl.Pass(Name="Dummy1", EndState=True, ResultAsJSON={"Value": "Dummy1"})
	p2 = awssl.Pass(Name="Dummy2", EndState=True, ResultAsJSON={"Value": "Dummy2"})
	p3 = awssl.Pass(Name="Dummy3", EndState=True, ResultAsJSON={"Value": "Dummy3"})

	# Attempt to retry any branch error using the defaults
	r = awssl.Retrier(ErrorNameList=["States.ALL"])

	# Run the branches in parallel, each having an individual retrier on any error returned
	para = awssl.ext.BranchRetryParallel(
		Name="MyParallel",
		BranchList=[p1,p2,p3],
		BranchRetryList=[r],
		FinallyState=finally_state,
		EndState=True)

	# Construct state machine
	sm = awssl.StateMachine(Comment="This is a test", StartState=para)
	return sm


if __name__ == "__main__":
	sm = branch_retry_parallel_state_example()
	print sm

