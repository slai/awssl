import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl
import awssl.ext

def for_state_example():

	# Declare the Arns for the Lambda functions required by awssl.ext.For
	awssl.ext.set_ext_arns(
		ForInitializer="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForExtractor="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForConsolidator="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForFinalizer="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		ForFinalizerParallelIterations="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		LimitedParallelConsolidator="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME")

	# Create the branch processing to be performed - in this case extraction of the iteration value
	p = awssl.Pass(Name="Dummy", EndState=True, OutputPath="$.iteration.Iteration")

	# Create 3 For instances to demonstrate the different From/To/Step features
	# Notice that the same branch definition can be reused across all the For loops
	s1 = awssl.ext.For(Name="For1", EndState=True,
		From=0, To=5, Step=1, BranchState=p, ParallelIteration=True)

	s2 = awssl.ext.For(Name="For2", EndState=True,
		From=0, To=8, Step=2, BranchState=p, ParallelIteration=True)

	s3 = awssl.ext.For(Name="For3", EndState=True,
		From=-16, To=16, Step=2, BranchState=p)

	# Run the For loops in parallel, to demonstrate there is no interdependencies
	para = awssl.Parallel(
		Name="Parallel-Fors",
		BranchList=[s1,s2,s3],
		EndState=True)

	# Construct state machine
	sm = awssl.StateMachine(Comment="This is a test")
	sm.set_start_state(para)
	return sm


if __name__ == "__main__":
	sm = for_state_example()
	print sm

