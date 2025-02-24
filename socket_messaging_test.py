# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020, Vathos GmbH
#
# All rights reserved.
#
###############################################################################

import logging
from unittest import TestCase, main
import socket

logging.getLogger(None).setLevel('DEBUG')


class TestSocketServer(TestCase):

  def setUp(self):
    self.host = 'staging.api.gke.vathos.net'
    self.port = 7052

  def test_test(self):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'test;4')
      data = s.recv(1024)
      data_string = data.decode('utf-8')
      print(data_string)
      data_split = data_string.split(';')
      data_type = int(data_split[0])
      # expects a string
      self.assertEqual(data_type, 0)
      print(data_split[1])
      self.assertEqual(data_split[1], 'Hello, world!\n')

  def test_get_pose(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'get_pose;votenet;ZYX;1;10')
      data = s.recv(1024)
      response_raw = data.decode('utf-8')
      response_parsed = response_raw.split(';')
      return_type = int(response_parsed[0])
      logging.debug('Got data type %d', return_type)
      # expect a pose
      self.assertEqual(return_type, 2)
      pose_parsed = [float(i) for i in response_parsed[1].split(',')]
      logging.debug('Got data %s', pose_parsed)

  def test_trigger(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'trigger;votenet;1;depth')
      data = s.recv(1024)
      data_string = data.decode('utf-8')
      response_parsed = data_string.split(';')
      return_type = int(response_parsed[0])
      # expect None
      self.assertEqual(return_type, 3)

  def test_save_image(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'save_image;depth;0;0.4,0.6,0.1,-0.24,3.0,-89.0;ZYX;1')
      data = s.recv(1024)
      data_string = data.decode('utf-8')
      response_parsed = data_string.split(';')
      return_type = int(response_parsed[0])
      # expect None
      self.assertEqual(return_type, 3)

  def test_load_configuration(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'load_configuration;65f03015416388eef98f2cc4;votenet')
      data = s.recv(1024)
      data_string = data.decode('utf-8')
      response_parsed = data_string.split(';')
      return_type = int(response_parsed[0])
      # expect None
      self.assertEqual(return_type, 3)

  def test_patch_configuration(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'patch_configuration;65f03015416388eef98f2cc4;key;0,foo')
      data = s.recv(1024)
      data_string = data.decode('utf-8')
      response_parsed = data_string.split(';')
      return_type = int(response_parsed[0])
      # expect None
      self.assertEqual(return_type, 3)

  def test_handeye_calibration(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(
          b'handeye_calibration;session;65f03015416388eef98f2cc4;vector;0;0;0.025;10;7;3d.handeye.calibration.vathos.net'
      )
      data = s.recv(1024)
      response_raw = data.decode('utf-8')
      response_parsed = response_raw.split(';')
      return_type = int(response_parsed[0])
      logging.debug('Got data type %d', return_type)
      # expect a pose
      self.assertEqual(return_type, 2)
      pose_parsed = [float(i) for i in response_parsed[1].split(',')]
      logging.debug('Got data %s', pose_parsed)
      self.assertEqual(pose_parsed, [0.3, -0.19, 0.7, 89.0, -2.3, 183.49])

  def test_get_number_of_detections(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'get_number_of_detections;votenet')
      data = s.recv(1024)
      response_raw = data.decode('utf-8')
      response_parsed = response_raw.split(';')
      return_type = int(response_parsed[0])
      result = int(response_parsed[1])
      logging.debug('Got data type %d', return_type)
      self.assertEqual(return_type, 5)
      self.assertEqual(result, 3)

  def test_estimate_surface_distance(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'estimate_surface_distance;votenet;250.0')
      data = s.recv(1024)
      response_raw = data.decode('utf-8')
      response_parsed = response_raw.split(';')
      return_type = int(response_parsed[0])
      result = float(response_parsed[1])
      logging.debug('Got result %f', result)
      self.assertEqual(return_type, 4)
      self.assertEqual(result, 0.837)

  def test_submit_pose(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'submit_pose;icp;0.4,0.6,0.1,-0.24,3.0,-89.0;vector;0;-1')
      data = s.recv(1024)
      response_raw = data.decode('utf-8')
      response_parsed = response_raw.split(';')
      return_type = int(response_parsed[0])
      self.assertEqual(return_type, 3)

  def test_get_item(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(b'get_item;magazine;0;1;2;ZYX;0;1')
      data = s.recv(1024)
      response_raw = data.decode('utf-8')
      response_parsed = response_raw.split(';')
      return_type = int(response_parsed[0])
      self.assertEqual(return_type, 2)
      pose_parsed = [float(i) for i in response_parsed[1].split(',')]
      logging.debug('Got data %s', pose_parsed)
      self.assertEqual(pose_parsed, [0.34, -0.12, 0.55, 2.3, 54.2, -88.9])

  def test_add_to_layer(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.host, self.port))
      s.sendall(
          b'add_to_layer;palletizing;0.4,0.6,0.1,-0.24,3.0,-89.0;0.4,0.6,0.1,-0.24,3.0,-89.0;0;1;2;vector;0'
      )
      data = s.recv(1024)
      response_raw = data.decode('utf-8')
      response_parsed = response_raw.split(';')
      return_type = int(response_parsed[0])
      self.assertEqual(return_type, 3)


if __name__ == '__main__':
  main()
