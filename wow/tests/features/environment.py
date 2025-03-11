"""
Environment setup for BDD tests.
"""
import os
import sys
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def before_all(context):
    """
    Set up the test environment before all tests.
    """
    logger.info("Setting up test environment")
    context.config.setup_logging()


def after_all(context):
    """
    Clean up the test environment after all tests.
    """
    logger.info("Cleaning up test environment")


def before_feature(context, feature):
    """
    Set up the test environment before each feature.
    """
    logger.info(f"Running feature: {feature.name}")


def after_feature(context, feature):
    """
    Clean up the test environment after each feature.
    """
    logger.info(f"Completed feature: {feature.name}")


def before_scenario(context, scenario):
    """
    Set up the test environment before each scenario.
    """
    logger.info(f"Running scenario: {scenario.name}")


def after_scenario(context, scenario):
    """
    Clean up the test environment after each scenario.
    """
    logger.info(f"Completed scenario: {scenario.name}")
