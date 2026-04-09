"use client";

import React, { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import ReactMarkdown from 'react-markdown';
import {
  ShieldCheck,
  Database,
  AlertTriangle,
  CheckCircle2,
  Play,
  Bot,
  FileCode2,
  Lock,
  History,
  Activity
} from 'lucide-react';

// Initialize Supabase Client
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

export default function Dashboard() {
  const [reports, setReports] = useState<any[]>([]);
  const [selectedReport, setSelectedReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('report');

  useEffect(() => {
    fetchReports();
  }, []);

  async function fetchReports() {
    const { data, error } = await supabase
      .from('governance_reports')
      .select('*')
      .order('audit_date', { ascending: false });

    if (!error && data) {
      setReports(data);
      if (data.length > 0) setSelectedReport(data[0]);
    }
    setLoading(false);
  }

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-black text-amber-500">
        <Activity size={48} className="animate-pulse" />
      </div>
    );
  }

  return (
    <div className="flex h-screen w-full bg-black text-zinc-300 font-sans overflow-hidden">

      {/* SIDEBAR: DYNAMIC SUPABASE REPORTS */}
      <aside className="w-72 bg-zinc-950 border-r border-zinc-800 flex flex-col z-10">
        <div className="h-16 flex items-center px-6 border-b border-zinc-800 bg-black/50">
          <ShieldCheck className="text-amber-500 mr-3" size={24} />
          <h1 className="text-lg font-bold text-white tracking-wide">GovEngine AI</h1>
        </div>

        <div className="p-4">
          <button className="w-full bg-amber-500 hover:bg-amber-400 text-black py-2.5 px-4 rounded-lg flex items-center justify-center gap-2 font-bold transition-all shadow-[0_0_15px_rgba(245,158,11,0.25)]">
            <Play size={16} fill="currentColor" />
            Trigger New Audit
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-2 space-y-2">
          <p className="text-xs font-bold text-zinc-500 uppercase tracking-wider mb-3 px-3 mt-4 flex items-center gap-2">
            <History size={14} /> Audit History
          </p>
          {reports.map((report) => (
            <button
              key={report.id}
              onClick={() => setSelectedReport(report)}
              className={`w-full flex flex-col text-left px-4 py-3 rounded-xl transition-all ${selectedReport?.id === report.id
                  ? 'bg-zinc-900 border border-zinc-700 shadow-sm'
                  : 'hover:bg-zinc-900/50 border border-transparent opacity-60 hover:opacity-100'
                }`}
            >
              <div className="flex items-center justify-between w-full">
                <span className="font-medium text-zinc-200 text-sm truncate pr-2">{report.target_file}</span>
                {selectedReport?.id === report.id ? <CheckCircle2 size={14} className="text-amber-500 flex-shrink-0" /> : <CheckCircle2 size={14} className="text-zinc-600 flex-shrink-0" />}
              </div>
              <span className="text-xs text-zinc-500 mt-1">
                {new Date(report.audit_date).toLocaleString()}
              </span>
            </button>
          ))}
        </nav>
      </aside>

      {/* MAIN CONTENT */}
      {selectedReport ? (
        <main className="flex-1 flex flex-col h-full overflow-hidden bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-zinc-900 via-black to-black">

          {/* TOP HEADER */}
          <header className="h-16 flex items-center justify-between px-8 border-b border-zinc-800/60 backdrop-blur-md">
            <div className="flex items-center gap-6">
              <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                <FileCode2 size={20} className="text-amber-500" />
                Audit Results: {selectedReport.target_file}
              </h2>
              <span className="px-3 py-1 text-xs font-bold bg-amber-500/10 text-amber-500 border border-amber-500/20 rounded-full flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
                Cleaned & Masked
              </span>
            </div>
            <div className="flex items-center gap-3 text-sm text-zinc-400">
              <Database size={16} className="text-blue-500" />
              Supabase Connected
            </div>
          </header>

          <div className="flex-1 overflow-y-auto p-8">
            <div className="max-w-6xl mx-auto space-y-8">

              {/* METRICS ROW */}
              <div className="grid grid-cols-3 gap-6">
                <div className="bg-zinc-950/50 border border-zinc-800 p-6 rounded-2xl flex flex-col relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                  <span className="text-zinc-400 text-sm font-medium mb-2">Dataset Health</span>
                  <div className="flex items-end gap-3">
                    <span className="text-4xl font-bold text-white">92</span>
                    <span className="text-amber-500 text-sm font-medium mb-1">/ 100</span>
                  </div>
                </div>

                <div className="bg-zinc-950/50 border border-zinc-800 p-6 rounded-2xl flex flex-col relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-red-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                  <span className="text-zinc-400 text-sm font-medium mb-2 flex items-center gap-2">
                    <Lock size={14} className="text-red-500" /> POPIA Risks Found
                  </span>
                  <div className="text-4xl font-bold text-white">3</div>
                </div>

                <div className="bg-zinc-950/50 border border-zinc-800 p-6 rounded-2xl flex flex-col relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                  <span className="text-zinc-400 text-sm font-medium mb-2">Rows Remediated</span>
                  <div className="text-4xl font-bold text-white">1,450</div>
                </div>
              </div>

              {/* SPLIT LAYOUT */}
              <div className="grid grid-cols-3 gap-8">

                {/* LEFT: DYNAMIC SUPABASE REPORT CONTENT */}
                <div className="col-span-2 space-y-4">
                  <div className="flex gap-4 border-b border-zinc-800">
                    <button
                      onClick={() => setActiveTab('report')}
                      className={`pb-3 px-2 text-sm font-bold transition-colors ${activeTab === 'report' ? 'text-amber-500 border-b-2 border-amber-500' : 'text-zinc-500 hover:text-zinc-300'}`}
                    >
                      Executive Summary
                    </button>
                    <button
                      onClick={() => setActiveTab('data')}
                      className={`pb-3 px-2 text-sm font-bold transition-colors ${activeTab === 'data' ? 'text-amber-500 border-b-2 border-amber-500' : 'text-zinc-500 hover:text-zinc-300'}`}
                    >
                      Remediation Preview
                    </button>
                  </div>

                  {activeTab === 'report' ? (
                    <div className="bg-zinc-950/80 border border-zinc-800 rounded-2xl p-8 text-zinc-300 leading-relaxed shadow-xl prose prose-invert prose-amber max-w-none">
                      {/* ReactMarkdown renders the ACTUAL text from your Python AI Agent */}
                      <ReactMarkdown>{selectedReport.report_content}</ReactMarkdown>
                    </div>
                  ) : (
                    <div className="bg-zinc-950/80 border border-zinc-800 rounded-2xl overflow-hidden shadow-xl">
                      <table className="w-full text-left text-sm">
                        <thead className="bg-zinc-900 text-zinc-400 border-b border-zinc-800">
                          <tr>
                            <th className="px-6 py-4 font-medium">user_id</th>
                            <th className="px-6 py-4 font-medium">sa_id <span className="text-amber-500 ml-1 text-xs">Masked</span></th>
                            <th className="px-6 py-4 font-medium">email</th>
                            <th className="px-6 py-4 font-medium">age <span className="text-amber-500 ml-1 text-xs">Filled</span></th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-zinc-800 text-zinc-300">
                          <tr className="hover:bg-zinc-900/50">
                            <td className="px-6 py-4">U-9021</td>
                            <td className="px-6 py-4 text-amber-500 font-mono">XXX-XXX-XXXX</td>
                            <td className="px-6 py-4">j.doe@company.za</td>
                            <td className="px-6 py-4">34</td>
                          </tr>
                          <tr className="hover:bg-zinc-900/50 bg-black/20">
                            <td className="px-6 py-4">U-9022</td>
                            <td className="px-6 py-4 text-amber-500 font-mono">XXX-XXX-XXXX</td>
                            <td className="px-6 py-4 text-amber-500">Unknown</td>
                            <td className="px-6 py-4">28</td>
                          </tr>
                          <tr className="hover:bg-zinc-900/50">
                            <td className="px-6 py-4">U-9023</td>
                            <td className="px-6 py-4 text-amber-500 font-mono">XXX-XXX-XXXX</td>
                            <td className="px-6 py-4">s.smith@mail.com</td>
                            <td className="px-6 py-4 text-amber-500">0</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>

                {/* RIGHT: AGENT ACTIVITY LOG */}
                <div className="col-span-1">
                  <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-6 shadow-xl sticky top-8">
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-6 flex items-center gap-2">
                      <Bot size={16} className="text-amber-500" />
                      Agent Activity Log
                    </h3>

                    <div className="space-y-6 relative before:absolute before:inset-0 before:ml-[11px] before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-zinc-800 before:to-transparent">

                      <div className="relative flex items-start gap-4">
                        <div className="absolute left-0 w-6 h-6 rounded-full bg-black border-2 border-zinc-800 flex items-center justify-center z-10">
                          <div className="w-2 h-2 rounded-full bg-zinc-600"></div>
                        </div>
                        <div className="ml-10 w-full">
                          <h4 className="text-sm font-bold text-zinc-200">Privacy Officer</h4>
                          <p className="text-xs text-zinc-400 mt-1">Scanned <code className="text-amber-500">{selectedReport.target_file}</code> for POPIA violations.</p>
                        </div>
                      </div>

                      <div className="relative flex items-start gap-4">
                        <div className="absolute left-0 w-6 h-6 rounded-full bg-black border-2 border-red-500/50 flex items-center justify-center z-10">
                          <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
                        </div>
                        <div className="ml-10 w-full">
                          <h4 className="text-sm font-bold text-red-500">Human-in-the-Loop</h4>
                          <p className="text-xs text-red-400 mt-1 bg-red-950/30 p-2 rounded border border-red-900/50">"Approval granted. Proceed with pipeline."</p>
                        </div>
                      </div>

                      <div className="relative flex items-start gap-4">
                        <div className="absolute left-0 w-6 h-6 rounded-full bg-black border-2 border-amber-500/50 flex items-center justify-center z-10">
                          <div className="w-2 h-2 rounded-full bg-amber-500"></div>
                        </div>
                        <div className="ml-10 w-full">
                          <h4 className="text-sm font-bold text-zinc-200">Data Quality Engineer</h4>
                          <p className="text-xs text-zinc-400 mt-1">Analysed schema integrity and filled <code className="text-amber-500">1,450</code> missing values.</p>
                        </div>
                      </div>

                      <div className="relative flex items-start gap-4">
                        <div className="absolute left-0 w-6 h-6 rounded-full bg-black border-2 border-green-500/50 flex items-center justify-center z-10">
                          <div className="w-2 h-2 rounded-full bg-green-500"></div>
                        </div>
                        <div className="ml-10 w-full">
                          <h4 className="text-sm font-bold text-zinc-200">Governance Communicator</h4>
                          <p className="text-xs text-zinc-400 mt-1">Executive report written and saved to Supabase.</p>
                        </div>
                      </div>

                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </main>
      ) : (
        <main className="flex-1 flex items-center justify-center bg-black">
          <div className="text-center text-zinc-600">
            <AlertTriangle size={48} className="mx-auto mb-4 text-zinc-700" />
            <p className="text-lg font-medium">No audit reports found.</p>
            <p className="text-sm mt-1">Trigger your first audit to get started.</p>
          </div>
        </main>
      )}

    </div>
  );
}