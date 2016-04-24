'use strict';

/**
 * @ngdoc function
 * @name yapp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of yapp
 */
angular.module('yapp')
  .controller('TimelineCtrl', function($scope, $http) {
  /*$scope.events = [{
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-check',
    title: 'First heading',
    content: 'Some awesome content.'
  }, {
    badgeClass: 'warning',
    badgeIconClass: 'glyphicon-credit-card',
    title: 'Second heading',
    content: 'More awesome content.'
  }];*/
  $http.get('http://54.86.178.90:5000/timeline').
    success(function(data) {
    $scope.mydata = data;
  });
  $scope.badgeClass = 'glyphicon-calendar';
  $scope.badgeInfo = 'info';
  $scope.appointments =
  [{
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 6 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-05-01 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 10 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-05-28 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 14 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-06-24 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 18 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-07-21 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 22 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-08-17 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 26 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-09-13 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 28 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-09-27 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 30 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-10-11 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 32 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-10-25 8:30PM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 34 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-11-8 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 36 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-11-22 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 37 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-11-29 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 38 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-12-13 8:30 AM'}
  },
  {
    badgeClass: 'info',
    badgeIconClass: 'glyphicon-calendar',
    summary: 'Your OBGYN Week 39 appointment with Dr. Bonnie Buttercup',
    appointmentDate: {day: 'monday',
    date: '2016-12-13 8:30 AM'}
  }];
  $scope.scheduleAppointment = function($scope) {
    window.alert('Next Appointment available for Aug 4, 2016 for 8:30 AM');
  };
  $scope.animateElementIn = function($el) {
    $el.removeClass('timeline-hidden');
    $el.addClass('bounce-in');
  };
  $scope.animateElementOut = function($el) {
    $el.addClass('timeline-hidden');
    $el.removeClass('bounce-in');
  };
  /*$scope.add = function() {
    $http.get()
    .success(function(data) {
    $scope.mydata = data;
    });
    $http.get('http://54.86.178.90:5000/book').
    success(function(data) {
    $scope.mydata = data;
  });
  };*/
});
