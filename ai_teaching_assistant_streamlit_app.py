import React, { useMemo, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Brain, Briefcase, Sparkles, TrendingUp, Target, BookOpen, ShieldCheck } from "lucide-react";
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";

const careerSkillModels = {
  "Data Analyst": {
    analytics: 92,
    technology: 85,
    communication: 72,
    adaptability: 78,
    leadership: 48,
    creativity: 66,
  },
  "Product Manager": {
    analytics: 74,
    technology: 68,
    communication: 88,
    adaptability: 84,
    leadership: 80,
    creativity: 76,
  },
  "AI Business Strategist": {
    analytics: 90,
    technology: 88,
    communication: 79,
    adaptability: 90,
    leadership: 70,
    creativity: 71,
  },
  "UX Researcher": {
    analytics: 65,
    technology: 54,
    communication: 84,
    adaptability: 74,
    leadership: 52,
    creativity: 90,
  },
};

const learningResources = {
  analytics: ["Excel & BI Analytics", "SQL Foundations", "Applied Statistics"],
  technology: ["Python for Business", "AI Literacy", "Cloud & Data Tools"],
  communication: ["Business Communication", "Presentation Skills", "Stakeholder Storytelling"],
  adaptability: ["Agile Problem Solving", "Scenario Planning", "Change Readiness"],
  leadership: ["Project Leadership", "Team Management Basics", "Decision-Making in Uncertainty"],
  creativity: ["Design Thinking", "Innovation Strategy", "Product Ideation Workshop"],
};

function clamp(value) {
  return Math.max(0, Math.min(100, Math.round(value)));
}

function buildStudentProfile({ gpa, studyHours, aiLiteracy, communication, stressManagement, teamwork }) {
  return {
    analytics: clamp(gpa * 18 + studyHours * 2 + aiLiteracy * 0.15),
    technology: clamp(aiLiteracy * 0.85 + studyHours * 1.8),
    communication: clamp(communication),
    adaptability: clamp((stressManagement + teamwork) / 2 + studyHours * 0.7),
    leadership: clamp(teamwork * 0.75 + communication * 0.25),
    creativity: clamp((communication * 0.35 + stressManagement * 0.25 + aiLiteracy * 0.3) * 0.9),
  };
}

function calculateReadiness(student, career) {
  const target = careerSkillModels[career];
  const keys = Object.keys(target);

  const gaps = keys.map((key) => ({
    skill: key,
    current: student[key],
    target: target[key],
    gap: clamp(target[key] - student[key]),
  }));

  const readiness = Math.round(
    keys.reduce((sum, key) => {
      const ratio = Math.min(student[key] / target[key], 1);
      return sum + ratio;
    }, 0) / keys.length * 100
  );

  return { readiness, gaps: gaps.sort((a, b) => b.gap - a.gap) };
}

function getMilestones(gaps) {
  const priority = gaps.filter((g) => g.gap > 0).slice(0, 3);
  if (priority.length === 0) {
    return [
      "Maintain your current profile with advanced projects.",
      "Add an industry certification to strengthen marketability.",
      "Build a portfolio demonstrating real-world readiness.",
    ];
  }
  return priority.map((item, index) => `Phase ${index + 1}: Improve ${item.skill} through ${learningResources[item.skill]?.[0] || "targeted learning"}.`);
}

export default function AILearningTwinPrototype() {
  const [name, setName] = useState("Daksha");
  const [career, setCareer] = useState("AI Business Strategist");
  const [gpa, setGpa] = useState(3.8);
  const [studyHours, setStudyHours] = useState([18]);
  const [aiLiteracy, setAiLiteracy] = useState([72]);
  const [communication, setCommunication] = useState([76]);
  const [stressManagement, setStressManagement] = useState([68]);
  const [teamwork, setTeamwork] = useState([80]);

  const studentProfile = useMemo(
    () =>
      buildStudentProfile({
        gpa,
        studyHours: studyHours[0],
        aiLiteracy: aiLiteracy[0],
        communication: communication[0],
        stressManagement: stressManagement[0],
        teamwork: teamwork[0],
      }),
    [gpa, studyHours, aiLiteracy, communication, stressManagement, teamwork]
  );

  const result = useMemo(() => calculateReadiness(studentProfile, career), [studentProfile, career]);

  const radarData = Object.keys(studentProfile).map((key) => ({
    skill: key.charAt(0).toUpperCase() + key.slice(1),
    student: studentProfile[key],
    target: careerSkillModels[career][key],
  }));

  const gapBars = result.gaps.map((g) => ({
    skill: g.skill.charAt(0).toUpperCase() + g.skill.slice(1),
    gap: g.gap,
  }));

  const topLearningRecommendations = result.gaps
    .filter((g) => g.gap > 0)
    .slice(0, 3)
    .flatMap((g) => learningResources[g.skill]?.slice(0, 2) || []);

  const milestones = getMilestones(result.gaps);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50 p-6 md:p-10">
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-200">
              <Sparkles className="h-4 w-4" /> AI Learning Twin Prototype
            </div>
            <h1 className="text-4xl font-bold mt-3 tracking-tight">Predictive Learning & Career Readiness Dashboard</h1>
            <p className="text-slate-300 mt-2 max-w-3xl">
              This prototype demonstrates how an AI Learning Twin could model a student profile, compare it against a future career target,
              identify skill gaps, and generate a personalized action plan.
            </p>
          </div>
          <Badge className="text-base px-4 py-2 rounded-full bg-emerald-500/20 text-emerald-200 border border-emerald-400/30">
            Readiness Score: {result.readiness}%
          </Badge>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          <Card className="lg:col-span-1 bg-slate-900 border-slate-800 rounded-3xl shadow-2xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><Brain className="h-5 w-5 text-cyan-300" /> Student Input Profile</CardTitle>
              <CardDescription>Enter baseline learner data to generate the AI Learning Twin.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-5">
              <div className="space-y-2">
                <Label>Name</Label>
                <Input value={name} onChange={(e) => setName(e.target.value)} className="bg-slate-950 border-slate-700" />
              </div>

              <div className="space-y-2">
                <Label>Target Career</Label>
                <Select value={career} onValueChange={setCareer}>
                  <SelectTrigger className="bg-slate-950 border-slate-700">
                    <SelectValue placeholder="Select a career" />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.keys(careerSkillModels).map((option) => (
                      <SelectItem key={option} value={option}>{option}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>GPA</Label>
                <Input type="number" min="0" max="4.3" step="0.1" value={gpa} onChange={(e) => setGpa(Number(e.target.value))} className="bg-slate-950 border-slate-700" />
              </div>

              {[
                ["Weekly Study Hours", studyHours, setStudyHours],
                ["AI / Tech Literacy", aiLiteracy, setAiLiteracy],
                ["Communication", communication, setCommunication],
                ["Stress Management", stressManagement, setStressManagement],
                ["Teamwork", teamwork, setTeamwork],
              ].map(([label, value, setter]) => (
                <div key={label} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <Label>{label}</Label>
                    <span className="text-slate-300">{value[0]}</span>
                  </div>
                  <Slider value={value} onValueChange={setter} max={100} step={1} />
                </div>
              ))}
            </CardContent>
          </Card>

          <div className="lg:col-span-2 grid gap-6">
            <div className="grid md:grid-cols-4 gap-4">
              {[
                { title: "Target Role", value: career, icon: Briefcase },
                { title: "Top Gap", value: result.gaps[0]?.skill || "None", icon: Target },
                { title: "Recommended Path", value: topLearningRecommendations[0] || "Advanced projects", icon: BookOpen },
                { title: "Risk Level", value: result.readiness >= 80 ? "Low" : result.readiness >= 60 ? "Moderate" : "High", icon: ShieldCheck },
              ].map((item) => {
                const Icon = item.icon;
                return (
                  <Card key={item.title} className="bg-slate-900 border-slate-800 rounded-3xl">
                    <CardContent className="p-5">
                      <div className="flex items-center justify-between mb-3">
                        <p className="text-sm text-slate-400">{item.title}</p>
                        <Icon className="h-5 w-5 text-cyan-300" />
                      </div>
                      <p className="font-semibold text-lg leading-tight">{item.value}</p>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            <div className="grid xl:grid-cols-2 gap-6">
              <Card className="bg-slate-900 border-slate-800 rounded-3xl">
                <CardHeader>
                  <CardTitle>Profile vs Future Role</CardTitle>
                  <CardDescription>Your current learning twin compared to the target career model.</CardDescription>
                </CardHeader>
                <CardContent className="h-[320px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData}>
                      <PolarGrid stroke="#334155" />
                      <PolarAngleAxis dataKey="skill" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
                      <PolarRadiusAxis tick={{ fill: "#94a3b8", fontSize: 10 }} domain={[0, 100]} />
                      <Radar name="Student" dataKey="student" stroke="#22d3ee" fill="#22d3ee" fillOpacity={0.35} />
                      <Radar name="Career Target" dataKey="target" stroke="#a78bfa" fill="#a78bfa" fillOpacity={0.15} />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="bg-slate-900 border-slate-800 rounded-3xl">
                <CardHeader>
                  <CardTitle>Skill Gap Forecast</CardTitle>
                  <CardDescription>Highest-priority gaps that need intervention.</CardDescription>
                </CardHeader>
                <CardContent className="h-[320px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={gapBars}>
                      <XAxis dataKey="skill" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
                      <YAxis tick={{ fill: "#94a3b8", fontSize: 12 }} />
                      <Tooltip />
                      <Bar dataKey="gap" radius={[10, 10, 0, 0]} fill="#22d3ee" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>

        <div className="grid xl:grid-cols-3 gap-6">
          <Card className="xl:col-span-1 bg-slate-900 border-slate-800 rounded-3xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-2"><TrendingUp className="h-5 w-5 text-cyan-300" /> Readiness Breakdown</CardTitle>
              <CardDescription>How prepared {name || "the student"} is for the selected future role.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Overall Career Readiness</span>
                  <span>{result.readiness}%</span>
                </div>
                <Progress value={result.readiness} className="h-3" />
              </div>
              {result.gaps.slice(0, 4).map((item) => (
                <div key={item.skill} className="space-y-1">
                  <div className="flex justify-between text-sm capitalize">
                    <span>{item.skill}</span>
                    <span>{item.current}/{item.target}</span>
                  </div>
                  <Progress value={Math.min((item.current / item.target) * 100, 100)} className="h-2" />
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="xl:col-span-1 bg-slate-900 border-slate-800 rounded-3xl">
            <CardHeader>
              <CardTitle>Recommended Learning Path</CardTitle>
              <CardDescription>Targeted interventions generated by the AI Learning Twin.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {topLearningRecommendations.length ? topLearningRecommendations.map((item, idx) => (
                <div key={idx} className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                  <div className="text-sm text-cyan-300 mb-1">Recommendation {idx + 1}</div>
                  <div className="font-medium">{item}</div>
                </div>
              )) : (
                <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">No critical gaps found. Focus on advanced projects and leadership exposure.</div>
              )}
            </CardContent>
          </Card>

          <Card className="xl:col-span-1 bg-slate-900 border-slate-800 rounded-3xl">
            <CardHeader>
              <CardTitle>Action Plan & Milestones</CardTitle>
              <CardDescription>A phased roadmap from education to career readiness.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {milestones.map((item, idx) => (
                <div key={idx} className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                  <div className="text-sm text-cyan-300 mb-1">Milestone {idx + 1}</div>
                  <div className="font-medium">{item}</div>
                </div>
              ))}
              <Button className="w-full rounded-2xl mt-2">Generate Updated Twin Report</Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
