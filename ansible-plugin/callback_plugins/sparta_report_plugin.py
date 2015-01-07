# Adapted from https://github.com/ansible/ansible/blob/devel/plugins/callbacks/log_plays.py
# And https://gist.github.com/cliffano/9868180

import os
import socket
from json import JSONEncoder
from datetime import datetime

datenow = datetime.now()
datenow = datenow.strftime('%Y-%m-%d-%h-%m-%s')
report_dir = "./report/"

#FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout', 'stderr']

STATIC_UP = """<html ng-app="reportingApp">
<head>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
<title>I/O Testing Report</title>
<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/css/bootstrap.min.css">
<!--link rel="stylesheet" href="dashboard.css"-->
<style>
    /* Move down content because we have a fixed navbar that is 50px tall */
    body {
        padding-top: 50px;
    }

    /*
     * Global add-ons
     */

    .sub-header {from ansible import utils
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }

    /*
     * Top navigation
     * Hide default border to remove 1px line.
     */
    .navbar-fixed-top {
        border: 0;
    }

    /*
     * Sidebar
     */

    /* Hide for mobile, show later */
    .sidebar {
        display: none;
    }

    @media (min-width: 768px) {
        .sidebar {
            position: fixed;
            top: 51px;
            bottom: 0;
            left: 0;
            z-index: 1000;
            display: block;
            padding: 20px;
            overflow-x: hidden;
            overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
            background-color: #f5f5f5;
            border-right: 1px solid #eee;
        }
    }

    /* Sidebar navigation */
    .nav-sidebar {
        margin-right: -21px; /* 20px padding + 1px border */
        margin-bottom: 20px;
        margin-left: -20px;
    }

    .nav-sidebar > li > a {
        padding-right: 20px;
        padding-left: 20px;
    }

    .nav-sidebar > .active > a,
    .nav-sidebar > .active > a:hover,
    .nav-sidebar > .active > a:focus {
        color: #fff;
        background-color: #428bca;
    }

    /*
     * Main content
     */

    .main {
        padding: 20px;
    }

    @media (min-width: 768px) {
        .main {
            padding-right: 40px;
            padding-left: 40px;
        }
    }

    .main .page-header {
        margin-top: 0;
    }

    /*
     * Placeholder dashboard ideas
     */

    .placeholders {
        margin-bottom: 30px;
        text-align: center;
    }

    .placeholders h4 {
        margin-bottom: 0;
    }

    .placeholder {
        margin-bottom: 20px;
    }

    .placeholder img {
        display: inline-block;
        border-radius: 50%;
    }
</style>
<script src="http://ajax.googleapis.com/ajax/libs/angularjs/1.2.20/angular.min.js"></script>
<script src="http://cdnjs.cloudflare.com/ajax/libs/angular-ui-bootstrap/0.10.0/ui-bootstrap-tpls.min.js"></script>
<!--script src="//cdnjs.cloudflare.com/ajax/libs/underscore.js/1.4.4/underscore-min.js"></script-->

<script src="http://cmaurer.github.io/angularjs-nvd3-directives/lib/d3/d3.min.js"></script>
<script src="http://cmaurer.github.io/angularjs-nvd3-directives/lib/nvd3/nv.d3.min.js"></script>
<link rel="stylesheet" href="http://cmaurer.github.io/angularjs-nvd3-directives/lib/nvd3/nv.d3.css">
<script src="http://cmaurer.github.io/angularjs-nvd3-directives/lib/angularjs-nvd3-directives/dist/angularjs-nvd3-directives.js"></script>
<script src="http://cmaurer.github.io/angularjs-nvd3-directives/javascripts/scale.fix.js"></script>
<script>
    var reportingApp = angular.module("reportingApp", ['ui.bootstrap', 'nvd3ChartDirectives']);
    reportingApp.controller("ReportCtrl", ['$scope', function ($scope) {
         $scope.report =
"""

STATIC_DOWN = """
 //========================================== featureCoverage ==========================================
        $scope.totalScenarios = 0;
        $scope.chartDataInit4featureCoverage = function () {
            $scope.report.features.forEach(function (f) {
                $scope.totalScenarios += f.scenarios ? f.scenarios.length : 0;
            });
            var totalAutomated = 0;
            $scope.report.features.forEach(function (f) {
                        if (f.scenarios) {
                            f.scenarios.forEach(function (s) {
                                totalAutomated += s.automated ? 1 : 0;
                            })
                        }
                    }
            );
            var automated = totalAutomated;
            var notAutomated = $scope.totalScenarios - totalAutomated;

            return [{x: 'Not yet automated', y: notAutomated, color: '#ED9C28'}, {
                x: 'Automated',
                y: automated,
                color: '#5CB85C'
            }];
        };
        $scope.chartData4featureCoverage = $scope.chartDataInit4featureCoverage();

        $scope.xFunction = function () {
            return function (d) {
                return d.x;
            };
        };
        $scope.yFunction = function () {
            return function (d) {
                return d.y;
            };
        };
        $scope.colorFunction = function () {
            return function (d) {
                return d.data.color;
            };
        };

        //========================================== featureSummary ==========================================
        $scope.buildSuccess = 0;
        $scope.chartDataInit4featureSummary = function () {
            var Failed = 0;
            var Passed = 0;
            var Skipped = 0;
            $scope.report.features.forEach(function (f) {
                        if (f.scenarios) {
                            f.scenarios.forEach(function (s) {
                                if (s.status && 'FAILED' === s.status.toUpperCase()) {
                                    Failed++;
                                } else if (s.status && 'PASSED' === s.status.toUpperCase()) {
                                    Passed++;
                                } else {
                                    Skipped++;
                                }
                            })
                        }
                    }
            );
            if(Failed ==0 && Passed ==0){
                return [];
            }else{
                $scope.buildSuccess = (Passed / (Passed + Failed))*100;
                return [{x: 'Failed', y: Failed, color: '#D2322D'}, {x: 'Passed', y: Passed, color: '#5CB85C'}
                , {x: 'Skipped', y: Skipped ,color:'#ED9C28'}
                ];
            }
        };
        $scope.chartData4featureSummary = $scope.chartDataInit4featureSummary();

        //========================================== caseSummary ==========================================
        $scope.totalCases = 0;
        $scope.chartDataInit4CaseSummary = function () {
            var Failed = 0;
            var Passed = 0;
            var Skipped = 0;
            $scope.report.features.forEach(function (f) {
                        if (f.scenarios) {
                            f.scenarios.forEach(function (s) {
                                if (s.cases) {
                                    s.cases.forEach(function (c) {
                                        $scope.totalCases++;
                                        if (c.status && 'FAILED' === c.status.toUpperCase()) {
                                            Failed++;
                                        } else if (c.status && 'PASSED' === c.status.toUpperCase()) {
                                            Passed++;
                                        } else {
                                            Skipped++;
                                        }
                                    })
                                }
                            })
                        }
                    }
            );
            if(Failed ==0 && Passed ==0){
                return [];
            }else{
                $scope.buildSuccess = (Passed / (Passed + Failed))*100;
                return [{x: 'Failed', y: Failed, color: '#D2322D'}, {x: 'Passed', y: Passed, color: '#5CB85C'}
                , {x: 'Skipped', y: Skipped ,color:'#ED9C28'}
                ];
            }
        };
        $scope.chartData4CaseSummary = $scope.chartDataInit4CaseSummary();

        //========================================== featureTable ==========================================
        $scope.featureRowColors = {Failed: 'danger', Passed: 'success', Skipped: 'warning'};

        $scope.featureSummaryTable = function () {
            var data = [];
            $scope.report.features.forEach(function (f) {
                        var Failed = 0;
                        var Passed = 0;
                        var Skipped = 0;
                        var Total = 0;
                        var scenarioSummary = [] ;
                        if (f.scenarios) {
                            f.scenarios.forEach(function (s) {
                                Total++;
                                if (s.status && 'FAILED' === s.status.toUpperCase()) {
                                    Failed++;
                                } else if (s.status && 'PASSED' === s.status.toUpperCase()) {
                                    Passed++;
                                } else {
                                    Skipped++;
                                }

                                var cFailed = 0;
                                var cPassed = 0;
                                var cSkipped = 0;
                                var cTotal = 0;
                                if (s.cases) {
                                    s.cases.forEach(function (c) {
                                        cTotal++;
                                        if (c.status && 'FAILED' === c.status.toUpperCase()) {
                                            cFailed++;
                                        } else if (c.status && 'PASSED' === c.status.toUpperCase()) {
                                            cPassed++;
                                        } else {
                                            cSkipped++;
                                        }
                                    })
                                }
                                scenarioSummary.push({name: s.name, Failed: cFailed, Passed: cPassed, Skipped: cSkipped, Total: cTotal})
                            })
                        }
                        data.push({name: f.name, Failed: Failed, Passed: Passed, Skipped: Skipped, Total: Total,
                                  scenario : scenarioSummary})
                    }
            );
            //console.log(data);
            return data;
        };
        $scope.featureSummaryTableData = $scope.featureSummaryTable();
        //Placeholder variables
        $scope.selectedFeature;
    }])
    ;
</script>
</head>

<body ng-controller="ReportCtrl">
<div>
    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                        data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">I/O Testing Report for {{ report.project.name }} Project</a>
            </div>
            <!--div class="navbar-collapse collapse">
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="#">Overview</a></li>
                </ul>
                <form class="navbar-form navbar-right">
                    <input class="form-control" placeholder="Search By Tags..." type="text">
                </form>
            </div-->
        </div>
    </div>

    <div class="container-fluid">
        <div class="row">
            <!--div class="col-sm-3 col-md-2 sidebar">
                <ul class="nav nav-sidebar">
                    <li class="active"><a href="#">Overview</a></li>
                    <li ng-repeat="feature in report.features">
                        <a href="#" ng-click="report.selectedFeature=feature.name">{{feature.name}}</a>
                    </li>
                </ul>
            </div>
            <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main"-->
            <div class="main">
                <h2 class="page-header">Automation execution Report of {{ report.project.name }} Project</h2>

                <div class="row">
                    <div class="col-sm-3"></div>
                    <div class="col-sm-6">
                        <alert type="danger" class="alert-danger" ng-show="report.signOffCommentsNegative
                                && buildSuccess < report.signOffSuccessThreshold"
                               close="report.signOffCommentsNegative=''">
                            <span class="glyphicon glyphicon-warning-sign"></span> {{report.signOffCommentsNegative}}
                        </alert>
                        <alert type="success" ng-show="report.signOffCommentsPositive
                            && buildSuccess >= report.signOffSuccessThreshold"
                               close="report.signOffCommentsPositive=''">
                            <span class="glyphicon glyphicon-ok"></span> {{report.signOffCommentsPositive}}
                        </alert>
                    </div>
                    <div class="col-sm-3"></div>
                </div>
                <div class="row" style="height: 300px" align="center">
                    <div class="col-sm-3">
                        <h4>Functional Automation Coverage</h4>
                        <span class="text-muted">Total Identified system features : {{report.features.length}} </span>
                        <nvd3-pie-chart
                                data="chartData4featureCoverage"
                                x="xFunction()"
                                y="yFunction()"
                                tooltips="true"
                                showLabels="true"
                                labelType="percent"
                                color="colorFunction()">
                            <svg></svg>
                        </nvd3-pie-chart>
                    </div>
                    <div class="col-sm-3">
                        <h4>Test Summary</h4>
                        <span class="text-muted">Total Identified scenarios: {{totalScenarios}}</span>
                        <nvd3-pie-chart
                                data="chartData4featureSummary"
                                x="xFunction()"
                                y="yFunction()"
                                tooltips="true"
                                showLabels="true"
                                labelType="percent"
                                noData="All tests skipped"
                                color="colorFunction()">
                            <svg></svg>
                        </nvd3-pie-chart>
                    </div>
                    <div class="col-sm-3">
                        <h4>Step Execution Summary</h4>
                        <span class="text-muted">Total Steps: {{totalCases}}</span>
                        <nvd3-pie-chart
                                data="chartData4CaseSummary"
                                x="xFunction()"
                                y="yFunction()"
                                tooltips="true"
                                showLabels="true"
                                labelType="percent"
                                noData="All tests skipped"
                                color="colorFunction()">
                            <svg></svg>
                        </nvd3-pie-chart>
                    </div>
                    <div class="col-sm-3">
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                <tr>
                                   <h6><th>Test Environment Details</th></h6>
                                </tr>
                                </thead>
                                <tbody>
                                <tr ng-repeat="v in report.environment.values">
                                    <td>{{v}}</td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <h3 class="sub-header">&nbsp;</h3>

                <h3 class="sub-header">Execution Statistics</h3>

                <tabset>
                    <tab>
                        <tab-heading>
                            Summary
                        </tab-heading>
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Feature</th>
                                    <th class="success">Passed</th>
                                    <th class="danger">Failed</th>
                                    <th class="warning">Skipped</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr ng-repeat="feature in featureSummaryTableData">
                                    <td>{{$index+1}}</td>
                                    <td>{{feature.name}}</td>
                                    <td class="success">{{feature.Passed}}</td>
                                    <td class="danger">{{feature.Failed}}</td>
                                    <td class="warning">{{feature.Skipped}}</td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </tab>
                    <tab>
                        <tab-heading>
                            Detail Execution status
                        </tab-heading>
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Feature / Scenario</th>
                                    <th>Tags</th>
                                    <th>Status</th>
                                    <th>Detail Status</th>
                                </tr>
                                </thead>
                                <tbody ng-repeat="feature in report.features">
                                  <tr ng-repeat-start="scenario in feature.scenarios"
                                    ng-class="featureRowColors[scenario.status]">
                                      <td><h6>{{$parent.$index+1}} / {{$index +1 }}</h6></td>
                                      <td><h6>{{feature.name}} / <b> {{scenario.name}} </b></h6></td>
                                      <td> <span ng-repeat="tag in feature.tags" class="label label-default">{{tag}}</span>
                                          <span ng-repeat="tag in scenario.tags"
                                                class="label label-default">{{tag}}</span></td>
                                      <td>{{scenario.status}}</td>
                                      <td><div class="row-fluid">
                                          <span class="col-sm-6">
                                            <progress animate="true" max="featureSummaryTableData[$parent.$index].scenario[$index].Total">
                                              <bar                  value="featureSummaryTableData[$parent.$parent.$index].scenario[$parent.$index].Passed"
                                                   type="success"> <span>{{featureSummaryTableData[$parent.$parent.$parent.$index].scenario[$parent.$parent.$index].Passed}}</span>
                                              </bar>
                                              <bar                 value="featureSummaryTableData[$parent.$parent.$index].scenario[$parent.$index].Failed"
                                                   type="danger"> <span>{{featureSummaryTableData[$parent.$parent.$parent.$index].scenario[$parent.$parent.$index].Failed}}</span>
                                              </bar>
                                              <bar                  value="featureSummaryTableData[$parent.$parent.$index].scenario[$parent.$index].Skipped"
                                                   type="warning"> <span>{{featureSummaryTableData[$parent.$parent.$parent.$index].scenario[$parent.$parent.$index].Skipped}}</span>
                                              </bar>
                                             </progress>
                                          </span>
                                          <span class="col-sm-3">
                                            <button type="button" class="btn btn-primary btn-sm" ng-click="showCaseDetails=!showCaseDetails">
                                                 Total {{ featureSummaryTableData[$parent.$index].scenario[$index].Total }} Steps
                                                 <i class="glyphicon" ng-class="{'glyphicon-chevron-down': showCaseDetails, 'glyphicon-chevron-right': !showCaseDetails}"></i>
                                            </button>
                                          </span>
                                      </div></td>
                                    </tr>
                                    <tr ng-repeat-end="" ng-show="showCaseDetails">
                                    <td></td>
                                    <td><b>Individual Test Result</b><i class="pull-right glyphicon glyphicon-chevron-right"></i></td>
                                    <td colspan="4">
                                      <div ng-repeat="case in scenario.cases"
                                      ng-class="{'text-warning': case.status=='Skipped', 'text-success': case.status=='Passed','text-danger': case.status=='Failed'}">
                                        <span class="glyphicon "
                                          ng-class="{'glyphicon-pause': case.status=='Skipped', 'glyphicon-ok': case.status=='Passed','glyphicon-remove': case.status=='Failed'}">
                                          </span> {{case.name}}
                                      </div>
                                    </td>
                                    <td></td>
                                    <td></td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </tab>
                    <tab>
                        <tab-heading>
                            <i class="glyphicon glyphicon-bell"></i> Failed Scenarios!
                        </tab-heading>
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Feature / Scenario</th>
                                    <th>Tags</th>
                                    <th>Status</th>
                                </tr>
                                </thead>
                                <tbody ng-repeat="feature in report.features">
                                <tr ng-repeat="scenario in feature.scenarios" ng-show="'Failed'==scenario.status"
                                    ng-class="featureRowColors[scenario.status]">
                                    <td><h6>{{$parent.$index+1}} / {{$index +1 }}</h6></td>
                                    <td><h6>{{feature.name}} / <b> {{scenario.name}} </b></h6></td>
                                    <td><span ng-repeat="tag in feature.tags" class="label label-default">{{tag}}</span>
                                        <span ng-repeat="tag in scenario.tags"
                                              class="label label-default">{{tag}}</span></td>
                                    <td>{{scenario.status}}</td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </tab>
                </tabset>
            </div>

        </div>
    </div>
</div>
</body>
</html>
"""

report = {
    "project": {},
    "environment": {},
    "signOffSuccessThreshold": 80,
    "signOffCommentsNegative": "Build Rejected. Build is not stable and Passed Test cases count is less than Accptable number/percentage",
    "signOffCommentsPositive": "Build Accepted",
    "features":[]
}


env_values = []
scenario_status = "Passed"

def find_feature(feature):
    for f in report["features"]:
        if f["name"] == feature["name"]:
            return f
    report["features"].append(feature)
    return feature

def find_scenario(scenarios, scenario):
    for s in scenarios:
        if s["name"] == scenario["name"]:
            return s
    scenarios.append(scenario)
    return scenario


def record_step(play, task, res, host, status):
    local_vars = play.vars
    if "project_name" in local_vars.keys():
        report["project"] = {"name": local_vars["project_name"]}
    if "environment" in local_vars.keys():
        env_values.append("Execution Date/Time: "+str(datetime.now()))
        env_values.append("Execution Environment: "+local_vars["environment"])
        env_values.append("TestMachine: "+socket.gethostname())
    if type(res) == type(dict()):
        if "cmd" in res.keys() and local_vars['scenario']:
            feature = find_feature({"name" : local_vars['feature'], "scenarios" : []})
            scenario = find_scenario(feature["scenarios"], {"name" : local_vars['scenario'], "cases" : []})
            scenario["cases"].append({"name": task, "status": status})
            if status == "Failed":
                scenario["status"] = "Failed"
            else:
                scenario["status"] = status

def write_report():
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    filnename = (report_dir + datenow + ".html")
    path = os.path.join(filnename)
    env_values.append("Results: "+path)
    report["environment"] = {"values": env_values}
    reportFile = open(path, "a")
    reportFile.write(STATIC_UP)
    reportFile.write(JSONEncoder().encode(report))
    reportFile.write(STATIC_DOWN)
    reportFile.close()


class CallbackModule(object):
    """
      logs playbook results, per host, as a basic html file in /var/log/ansible/hosts/html/
    """

    def __init__(self):
        self.disabled = False
        self.token = None
        self.printed_playbook = False
        self.playbook = None
        self.play = None
        self.playbook_name = None
        self.inventory = None
        self.task = None

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        record_step(self.play, self.task, res, host, "Failed")

    def runner_on_ok(self, host, res):
        record_step(self.play, self.task, res, host, "Passed")

    def runner_on_error(self, host, msg):
        #record_step(self.play, self.task, res, host, "Failed")
        pass

    def runner_on_skipped(self, host, item=None):
        #record_step(self.play, self.task, res, host, "Skipped")
        pass

    def runner_on_unreachable(self, host, res):
        record_step(self.play, self.task, res, host, "Failed")

    def runner_on_no_hosts(self):
        #record_step(self.play, self.task, res, host, "Skipped")
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        record_step(self.play, self.task, res, host, "Passed")

    def runner_on_async_ok(self, host, res, jid):
        record_step(self.play, self.task, res, host, "Passed")

    def runner_on_async_failed(self, host, res, jid):
        record_step(self.play, self.task, res, host, "Failed")

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        self.task = name

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None,
                                salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass

    def playbook_on_play_start(self, pattern):
        self.play = self.play


    def playbook_on_stats(self, stats):
        write_report()
